import dataclasses
from typing import List, Union, Optional
from enum import Enum

from .token import Token, KEYWORDS
from .ast import IntegerConstant, FloatingConstant
from .file import File, Location


class Error(Enum):
    UNKNOWN_CHARACTER = "unknown character"
    UNTERMINATED_MULTI_LINE_COMMENT = "unterminated /* comment"
    UNTERMINATED_STRING = "unterminated string"
    UNTERMINATED_CHARACTER = "unterminated character"
    INVALID_INTEGER_CONSTANT_SUFFIX = "invalid integer constant suffix"
    INVALID_FLOATING_CONSTANT_SUFFIX = "invalid floating constant suffix"
    INVALID_DIGIT = "invalid digit"
    INVALID_FLOATING_EXPONENT = "invalid floating exponent"


class Warning(Enum):
    UNKNOWN_ESCAPE_SEQUENCE = "unknown escape sequence"


@dataclasses.dataclass
class ErrorInfo:
    location: Location
    name: Union[Error, Warning]
    message: str


@dataclasses.dataclass
class Scanner:
    file: File
    pos: int = 0
    startpos: int = 0
    endpos: int = 0
    line: int = 1
    column: int = 0
    value: Union[IntegerConstant, FloatingConstant, None] = None
    errors: List[ErrorInfo] = dataclasses.field(default_factory=list)

    @property
    def text(self) -> str:
        return self.file.source[self.startpos : self.endpos]

    def _peek(self, off=0) -> str:
        pos = self.pos + off
        if pos < len(self.file.source):
            c = self.file.source[pos]
            return c
        return ""

    def _consume(self) -> None:
        self.pos += 1
        self.column += 1

    def _error(
        self, error: Union[Error, Warning], message: Optional[str] = None
    ) -> None:
        if message is None:
            message = error.value
        loc = Location(self.file.filename, self.pos, self.line, self.column)
        self.errors.append(ErrorInfo(loc, error, message))

    def scan(self):
        self._skip_whitespaces()
        self.startpos = self.pos
        self._loc = Location(self.file.filename, self.pos, self.line, self.column)
        tok = self._scan()
        self.endpos = self.pos
        return tok

    def _scan(self) -> Token:
        self.value = None

        c = self._peek()
        if c == "":
            return Token.EOF
        elif c.isdigit():
            return self._scan_number()

        self._consume()
        if c == "_" or c.isalpha():
            return self._scan_identifier()
        elif c == "{":
            return Token.LEFT_BRACE
        elif c == "}":
            return Token.RIGHT_BRACE
        elif c == "(":
            return Token.LEFT_PAREN
        elif c == ")":
            return Token.RIGHT_PAREN
        elif c == "[":
            return Token.LEFT_BRACKET
        elif c == "]":
            return Token.RIGHT_BRACKET
        elif c == ".":
            c2 = self._peek()
            if c2.isdigit():
                return self._scan_decimal_fractional_part()
            return Token.DOT
        elif c == ";":
            return Token.SEMICOLON
        elif c == ",":
            return Token.COMMA
        elif c == "<":
            c2 = self._peek()
            if c2 == "<":
                self._consume()
                c3 = self._peek()
                if c3 == "=":
                    self._consume()
                    return Token.LESS_THAN_LESS_THAN_EQUALS
                return Token.LESS_THAN_LESS_THAN
            elif c2 == "=":
                self._consume()
                return Token.LESS_THAN_EQUALS
            return Token.LESS_THAN
        elif c == ">":
            c2 = self._peek()
            if c2 == ">":
                self._consume()
                c3 = self._peek()
                if c3 == "=":
                    self._consume()
                    return Token.GREATER_THAN_GREATER_THAN_EQUALS
                return Token.GREATER_THAN_GREATER_THAN
            elif c2 == "=":
                self._consume()
                return Token.GREATER_THAN_EQUALS
            return Token.GREATER_THAN
        elif c == "=":
            c2 = self._peek()
            if c2 == "=":
                self._consume()
                return Token.EQUALS_EQUALS
            return Token.EQUALS
        elif c == "!":
            c2 = self._peek()
            if c2 == "=":
                self._consume()
                return Token.EXCLAMATION_EQUALS
            return Token.EXCLAMATION
        elif c == "+":
            c2 = self._peek()
            if c2 == "+":
                self._consume()
                return Token.PLUS_PLUS
            elif c2 == "=":
                self._consume()
                return Token.PLUS_EQUALS
            return Token.PLUS
        elif c == "-":
            c2 = self._peek()
            if c2 == "-":
                self._consume()
                return Token.MINUS_MINUS
            elif c2 == "=":
                self._consume()
                return Token.MINUS_EQUALS
            elif c2 == ">":
                self._consume()
                return Token.ARROW
            return Token.MINUS
        elif c == "*":
            c2 = self._peek()
            if c2 == "=":
                self._consume()
                return Token.STAR_EQUALS
            return Token.STAR
        elif c == "/":
            c2 = self._peek()
            if c2 == "/":
                self._consume()
                return self._scan_single_line_comment()
            elif c2 == "*":
                self._consume()
                return self._scan_multi_line_comment()
            elif c2 == "=":
                self._consume()
                return Token.SLASH_EQUALS
            return Token.SLASH
        elif c == "%":
            c2 = self._peek()
            if c2 == "=":
                self._consume()
                return Token.PERCENT_EQUALS
            return Token.PERCENT
        elif c == "&":
            c2 = self._peek()
            if c2 == "&":
                self._consume()
                return Token.AMPERSAND_AMPERSAND
            elif c2 == "=":
                self._consume()
                return Token.AMPERSAND_EQUALS
            return Token.AMPERSAND
        elif c == "|":
            c2 = self._peek()
            if c2 == "|":
                self._consume()
                return Token.PIPE_PIPE
            elif c2 == "=":
                self._consume()
                return Token.PIPE_EQUALS
            return Token.PIPE
        elif c == "^":
            c2 = self._peek()
            if c2 == "=":
                self._consume()
                return Token.CARET_EQUALS
            return Token.CARET
        elif c == "~":
            return Token.TILDE
        elif c == "?":
            return Token.QUESTION
        elif c == ":":
            return Token.COLON
        else:
            self._error(Error.UNKNOWN_CHARACTER)
            return Token.INVALID

    def _scan_identifier(self) -> Token:
        while True:
            c = self._peek()
            if c == "_" or c.isalnum():
                self._consume()
            else:
                break
        text = self.file.source[self.startpos : self.pos]
        return KEYWORDS.get(text, Token.IDENTIFIER)

    def _scan_number(self) -> Token:
        def is_digit(c):
            if c == "":
                return False
            return c.isdigit() or c in "abcdefABCDEF"

        startpos = self.startpos
        base = 10
        c = self._peek()
        if c == "0":
            self._consume()
            c2 = self._peek()
            if is_digit(c2):
                base = 8
                startpos = self.pos
            elif c2 == "x" or c2 == "X":
                c3 = self._peek(1)
                if is_digit(c3):
                    self._consume()
                    base = 16
                    startpos = self.pos
        invalid_digit = False
        while True:
            c = self._peek()
            if not is_digit(c):
                break
            if base != 16 and (c == "e" or c == "E"):
                return self._scan_decimal_fractional_part()
            if not invalid_digit:
                if base == 8 and c not in "01234567":
                    invalid_digit = True
                    self._error(
                        Error.INVALID_DIGIT, f"invalid digit '{c}' in octal constant"
                    )
                elif base == 10 and not c.isdigit():
                    invalid_digit = True
                    self._error(
                        Error.INVALID_DIGIT, f"invalid digit '{c}' in decimal constant"
                    )
            self._consume()
        if c == ".":
            self._consume()
            if base == 8 or base == 10:
                return self._scan_decimal_fractional_part()
            elif base == 16:
                return self._scan_hexadecimal_fractional_part()
        if base == 16 and (c == "p" or c == "P"):
            return self._scan_hexadecimal_fractional_part()
        endpos = self.pos
        suffix = self._scan_number_suffix()
        if invalid_digit:
            return Token.INVALID
        if not self._validate_integer_constant_suffix(suffix):
            self._error(
                Error.INVALID_INTEGER_CONSTANT_SUFFIX,
                f"invalid suffix '{suffix}' on integer constant",
            )
            return Token.INVALID
        self.value = IntegerConstant(
            self._loc,
            self.file.source[self.startpos : self.pos],
            int(self.file.source[startpos:endpos], base),
        )
        return Token.INTEGER_CONSTANT

    def _scan_number_suffix(self) -> str:
        startpos = self.pos
        c = self._peek()
        while c.isalnum() or c == ".":
            self._consume()
            c = self._peek()
        return self.file.source[startpos : self.pos]

    def _scan_decimal_fractional_part(self) -> Token:
        while True:
            c = self._peek()
            if not c.isdigit():
                break
            self._consume()
        invalid_exponent = False
        if c == "e" or c == "E":
            self._consume()
            c = self._peek()
            if c == "+" or c == "-":
                self._consume()
                c = self._peek()
            if not c.isdigit():
                invalid_exponent = True
                self._error(Error.INVALID_FLOATING_EXPONENT, f"exponent has no digits")
            while c.isdigit():
                self._consume()
                c = self._peek()
        endpos = self.pos
        suffix = self._scan_number_suffix()
        if invalid_exponent:
            return Token.INVALID
        elif suffix not in ("", "f", "l", "F", "L"):
            self._error(
                Error.INVALID_FLOATING_CONSTANT_SUFFIX,
                f"invalid suffix '{suffix}' on floating constant",
            )
            return Token.INVALID
        self.value = FloatingConstant(
            self._loc,
            self.file.source[self.startpos : self.pos],
            float(self.file.source[self.startpos : endpos]),
        )
        return Token.FLOATING_CONSTANT

    def _scan_hexadecimal_fractional_part(self) -> Token:
        def is_digit(c):
            if c == "":
                return False
            return c.isdigit() or c in "abcdefABCDEF"

        while True:
            c = self._peek()
            if not is_digit(c):
                break
            self._consume()
        invalid_exponent = False
        if c == "p" or c == "P":
            self._consume()
            c = self._peek()
            if c == "+" or c == "-":
                self._consume()
                c = self._peek()
            if not c.isdigit():
                invalid_exponent = True
                self._error(Error.INVALID_FLOATING_EXPONENT, f"exponent has no digits")
            while c.isdigit():
                self._consume()
                c = self._peek()
        else:
            invalid_exponent = True
            self._error(
                Error.INVALID_FLOATING_EXPONENT,
                "hexadecimal floating constant requires an exponent",
            )
        endpos = self.pos
        suffix = self._scan_number_suffix()
        if invalid_exponent:
            return Token.INVALID
        elif suffix not in ("", "f", "l", "F", "L"):
            self._error(
                Error.INVALID_FLOATING_CONSTANT_SUFFIX,
                f"invalid suffix '{suffix}' on floating constant",
            )
            return Token.INVALID
        self.value = FloatingConstant(
            self._loc,
            self.file.source[self.startpos : self.pos],
            float.fromhex(self.file.source[self.startpos : endpos]),
        )
        return Token.FLOATING_CONSTANT

    def _validate_integer_constant_suffix(self, suffix) -> bool:
        i = 0
        unsigned = False
        long = False
        while i < len(suffix):
            c = suffix[i]
            i += 1
            if c in "uU" and not unsigned:
                unsigned = True
            elif c in "lL" and not long:
                if i < len(suffix):
                    c2 = suffix[i]
                    if c2 == c:
                        i += 1
                long = True
            else:
                return False
        return True

    def _scan_single_line_comment(self) -> Token:
        while True:
            c = self._peek()
            if c == "":
                break
            elif c == "\r" or c == "\n":
                self._scan_newline()
                break
            self._consume()
        return Token.SINGLE_LINE_COMMENT

    def _scan_multi_line_comment(self) -> Token:
        while True:
            c = self._peek()
            if c == "":
                self._error(Error.UNTERMINATED_MULTI_LINE_COMMENT)
                return Token.INVALID
            elif c == "*":
                self._consume()
                c2 = self._peek()
                if c2 == "/":
                    self._consume()
                    return Token.MULTI_LINE_COMMENT
            elif c == "\r" or c == "\n":
                self._scan_newline()
            else:
                self._consume()

    def _skip_whitespaces(self) -> None:
        while True:
            c = self._peek()
            if not c.isspace():
                break
            if c == "\r" or c == "\n":
                self._scan_newline()
            else:
                self._consume()

    def _scan_newline(self) -> None:
        c = self._peek()
        if c == "\r":
            self._consume()
            if self._peek() == "\n":
                self._consume()
            self.line += 1
            self.column = 0
        elif c == "\n":
            self._consume()
            self.line += 1
            self.column = 0
