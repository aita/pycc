import dataclasses
from typing import List, Union

from . import ast
from .file import Location
from .token import Token
from .scanner import Scanner
from .error import Error, Warning, Reporter


class ParseError(Exception):
    pass


@dataclasses.dataclass(frozen=True)
class TokenData:
    kind: Token
    start: Location
    end: Location
    text: str
    value: Union[int, float, str, None]


@dataclasses.dataclass
class TokenStream:
    scanner: Scanner
    pos: int = dataclasses.field(default=0, init=False)
    buf: List[TokenData] = dataclasses.field(default_factory=list, init=False)
    markers: List[int] = dataclasses.field(default_factory=list, init=False)

    def LT(self, i: int) -> TokenData:
        self.sync(i)
        return self.buf[self.pos + i - 1]

    def LA(self, i: int) -> Token:
        return self.LT(i).kind

    def sync(self, i: int) -> None:
        if self.pos + i - 1 > len(self.buf) - 1:
            n = (self.pos + i - 1) - (len(self.buf) - 1)
            self.fill(n)

    def fill(self, n: int) -> None:
        for i in range(n):
            self.buf.append(self._scan())

    def _scan(self) -> Token:
        while True:
            tok = self.scanner.scan()
            if tok in (Token.SINGLE_LINE_COMMENT, Token.MULTI_LINE_COMMENT):
                continue
            return TokenData(
                tok,
                self.scanner.start,
                self.scanner.end,
                self.scanner.text,
                self.scanner.value,
            )

    def consume(self) -> None:
        self.pos += 1
        if self.pos == len(self.buf) and self.is_speculating():
            self.pos = 0
            self.buf.clear()
        self.sync(1)

    def mark(self) -> int:
        self.markers.append(self.pos)
        return self.pos

    def release(self) -> None:
        marker = self.markers.pop()
        self.seek(marker)

    def seek(self, index: int) -> None:
        self.pos = index

    def is_speculating(self) -> bool:
        return len(self.markers) > 0


@dataclasses.dataclass
class Parser:
    tokens: TokenStream
    reporter: Reporter

    def _expect(self, *tokens: List[Token]):
        if self.tokens.LA(1) in tokens:
            return
        if len(tokens) == 1:
            message = f"expected {tokens[0].value}"
        else:
            message = (
                "expected "
                + ", ".join([x.value for x in tokens[:-1]])
                + f"or {tokens[-1].value}"
            )
        self.reporter.error(self.tokens.LT(1).start, Error.UNEXPECTED_TOKEN, message)
        # self.tokens.consume()
        raise ParseError(message)

    def parse() -> ast.TranslationUnit:
        pass

    def parse_stmt(self) -> ast.Stmt:
        expr = self.parse_expr()
        self._expect(Token.SEMICOLON)
        semi = self.tokens.LT(1)
        self.tokens.consume()
        return ast.ExprStmt(expr.start, semi.end, expr)

    def parse_expr(self) -> ast.Expr:
        return self.parse_primary_expr()

    def parse_ref_decl_expr(self) -> ast.RefDeclExpr:
        self._expect(Token.IDENTIFIER)
        tok = self.tokens.LT(1)
        self.tokens.consume()
        return ast.RefDeclExpr(tok.start, tok.end, tok.value)

    def parse_primary_expr(self) -> ast.Expr:
        constants = {
            Token.INTEGER_CONSTANT: ast.IntegerConstant,
            Token.FLOATING_CONSTANT: ast.FloatingConstant,
            Token.CHARACTER_CONSTANT: ast.CharacterConstant,
            Token.STRING_CONSTANT: ast.StringConstant,
        }

        self._expect(Token.IDENTIFIER, Token.LEFT_PAREN, *constants.keys())
        tok = self.tokens.LT(1)
        if tok.kind == Token.IDENTIFIER:
            return self.parse_ref_decl_expr()
        elif tok.kind in constants:
            self.tokens.consume()
            return constants[tok.kind](tok.start, tok.end, tok.text, tok.value)
        elif tok.kind == Token.LEFT_PAREN:
            self.tokens.consume()
            e = self.parse_expr()
            rparen = self._expect(Token.RPAREN)
            self.tokens.consume()
            return ast.ParenExpr(tok.start, rparen.end, e)
