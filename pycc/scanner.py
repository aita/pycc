import dataclasses
from typing import Union
from io import StringIO

from .token import Token, KEYWORDS
from .file import File, Location
from .error import Error, Warning, Reporter


OCTAL_DIGIT = set("01234567")
HEXADECIMAL_DIGIT = set("0123456789abcdefABCDEF")

ESCAPES = {
    "'": "'",
    '"': '"',
    "?": "\x3F",
    "a": "\a",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "v": "\v",
    "\\": "\\",
}

_KEYWORDS = {x.value: x for x in KEYWORDS}


@dataclasses.dataclass
class Scanner:
    file: File
    reporter: Reporter
    pos: int = dataclasses.field(default=0, init=False)
    startpos: int = dataclasses.field(default=0, init=False)
    endpos: int = dataclasses.field(default=0, init=False)
    line: int = dataclasses.field(default=1, init=False)
    column: int = dataclasses.field(default=0, init=False)
    value: Union[int, float, str, None] = dataclasses.field(init=False)
    start: Location = dataclasses.field(init=False)
    end: Location = dataclasses.field(init=False)

    @property
    def text(self) -> str:
        return self.file.source[self.startpos : self.endpos]

    def _peek(self, off=0) -> str:
        pos = self.pos + off
        if pos < len(self.file.source):
            c = self.file.source[pos]
            return c
        return ""

    def _location(self):
        return Location(self.file.filename, self.pos, self.line, self.column)

    def _consume(self, off=1) -> None:
        self.pos += off
        self.column += off

    def scan(self):
        self._skip_whitespaces()
        self.startpos = self.pos
        self.start = self._location()
        tok = self._scan()
        self.endpos = self.pos
        self.end = self._location()
        return tok

    def _scan(self) -> Token:
        self.value = None

        c = self._peek()
        if c == "":
            return Token.EOF
        elif c.isdigit():
            return self._scan_number()

        self._consume()
        if c == "'":
            return self._scan_character_constant()
        elif c == '"':
            return self._scan_string_constant()
        elif c == "_" or c.isalpha():
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
            elif c2 == ".":
                c3 = self._peek(1)
                if c3 == ".":
                    self._consume(2)
                    return Token.ELLIPSIS
            return Token.PERIOD
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
            elif c2 == ":":
                self._consume()
                return Token.LEFT_BRACKET
            elif c2 == "%":
                self._consume()
                return Token.LEFT_BRACE
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
            elif c2 == ">":
                self._consume()
                return Token.RIGHT_BRACE
            elif c2 == ":":
                self._consume()
                c3 = self._peek()
                if c3 == "%":
                    c4 = self._peek(1)
                    if c4 == ":":
                        self._consume(2)
                        return Token.HASH_HASH
                return Token.HASH
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
            c2 = self._peek()
            if c2 == ">":
                self._consume()
                return Token.RIGHT_BRACKET
            return Token.COLON
        elif c == "#":
            c2 = self._peek()
            if c2 == "#":
                self._consume()
                return Token.HASH_HASH
            return Token.HASH
        else:
            self.reporter.error(self._location(), Error.UNKNOWN_CHARACTER)
            return Token.INVALID

    def _scan_identifier(self) -> Token:
        while True:
            c = self._peek()
            if c == "_" or c.isalnum():
                self._consume()
            else:
                break
        text = self.file.source[self.startpos : self.pos]
        return _KEYWORDS.get(text, Token.IDENTIFIER)

    def _scan_number(self) -> Token:
        startpos = self.startpos
        base = 10
        c = self._peek()
        if c == "0":
            self._consume()
            c2 = self._peek()
            if c2 in HEXADECIMAL_DIGIT:
                base = 8
                startpos = self.pos
            elif c2 == "x" or c2 == "X":
                c3 = self._peek(1)
                if c3 in HEXADECIMAL_DIGIT:
                    self._consume()
                    base = 16
                    startpos = self.pos
        invalid_digit = False
        while True:
            c = self._peek()
            if c not in HEXADECIMAL_DIGIT:
                break
            if base != 16 and (c == "e" or c == "E"):
                return self._scan_decimal_fractional_part()
            if not invalid_digit:
                if base == 8 and c not in "01234567":
                    invalid_digit = True
                    self.reporter.error(
                        self._location(),
                        Error.INVALID_DIGIT,
                        f"invalid digit '{c}' in octal constant",
                    )
                elif base == 10 and not c.isdigit():
                    invalid_digit = True
                    self.reporter.error(
                        self._location(),
                        Error.INVALID_DIGIT,
                        f"invalid digit '{c}' in decimal constant",
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
            self.reporter.error(
                self._location(),
                Error.INVALID_INTEGER_CONSTANT_SUFFIX,
                f"invalid suffix '{suffix}' on integer constant",
            )
            return Token.INVALID
        self.value = int(self.file.source[startpos:endpos], base)
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
                self.reporter.error(
                    self._location(),
                    Error.INVALID_FLOATING_EXPONENT,
                    f"exponent has no digits",
                )
            while c.isdigit():
                self._consume()
                c = self._peek()
        endpos = self.pos
        suffix = self._scan_number_suffix()
        if invalid_exponent:
            return Token.INVALID
        elif suffix not in ("", "f", "l", "F", "L"):
            self.reporter.error(
                self._location(),
                Error.INVALID_FLOATING_CONSTANT_SUFFIX,
                f"invalid suffix '{suffix}' on floating constant",
            )
            return Token.INVALID
        self.value = float(self.file.source[self.startpos : endpos])
        return Token.FLOATING_CONSTANT

    def _scan_hexadecimal_fractional_part(self) -> Token:
        while True:
            c = self._peek()
            if c not in HEXADECIMAL_DIGIT:
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
                self.reporter.error(
                    self._location(),
                    Error.INVALID_FLOATING_EXPONENT,
                    f"exponent has no digits",
                )
            while c.isdigit():
                self._consume()
                c = self._peek()
        else:
            invalid_exponent = True
            self.reporter.error(
                self._location(),
                Error.INVALID_FLOATING_EXPONENT,
                "hexadecimal floating constant requires an exponent",
            )
        endpos = self.pos
        suffix = self._scan_number_suffix()
        if invalid_exponent:
            return Token.INVALID
        elif suffix not in ("", "f", "l", "F", "L"):
            self.reporter.error(
                self._location(),
                Error.INVALID_FLOATING_CONSTANT_SUFFIX,
                f"invalid suffix '{suffix}' on floating constant",
            )
            return Token.INVALID
        self.value = float.fromhex(self.file.source[self.startpos : endpos])
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

    def _scan_character_constant(self) -> Token:
        try:
            self.value = self._scan_character_sequence("'")
        except ValueError:
            return Token.INVALID
        return Token.CHARACTER_CONSTANT

    def _scan_string_constant(self) -> Token:
        try:
            self.value = self._scan_character_sequence('"')
        except ValueError:
            return Token.INVALID
        return Token.STRING_CONSTANT

    def _scan_character_sequence(self, quote) -> str:
        out = StringIO()
        error = None
        while True:
            c = self._peek()
            if c != "":
                self._consume()
            if c == quote:
                break
            elif c == "\\":
                try:
                    out.write(self._scan_escape_sequence())
                except ValueError as e:
                    error = e
            elif c == "\r" or c == "\n" or c == "":
                message = "missing terminating ' character"
                self.reporter.error(
                    self._location(), Error.UNTERMINATED_CHARACTER, message
                )
                raise ValueError(message)
            else:
                out.write(c)
        if error:
            raise error
        return out.getvalue()

    def _scan_escape_sequence(self, csize=1) -> str:
        pos = self.pos
        c = self._peek()
        self._consume()
        if c in OCTAL_DIGIT:
            if self._peek() in OCTAL_DIGIT:
                self._consume()
                if self._peek() in OCTAL_DIGIT:
                    self._consume()
            return chr(int(self.file.source[pos : self.pos], 8))
        elif c == "x" or c == "X":
            self._consume()
            pos = self.pos
            while True:
                c = self._peek()
                if c not in HEXADECIMAL_DIGIT:
                    break
                self._consume()
            text = self.file.source[pos : self.pos]
            if len(text) == 0:
                message = r"\x used with no following hex digits"
                self.reporter.error(
                    self._location(), Error.INVALID_ESCAPE_SEQUENCE, message
                )
                raise ValueError(message)
            if len(text) > csize * 2:
                message = "hex escape sequence out of range"
                self.reporter.error(self._location(), Error.INVALID_ESCAPE_SEQUENCE)
                raise ValueError(message)
            return chr(int(text, 16))
        elif c == "\r" or c == "\n":
            self._scan_newline()
            return ""
        elif c in ESCAPES:
            return ESCAPES[c]
        self.reporter.warning(
            self._location(),
            Warning.UNKNOWN_ESCAPE_SEQUENCE,
            f"unknown escape sequence '\\{c}'",
        )
        return c

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
                self.reporter.error(
                    self._location(), Error.UNTERMINATED_MULTI_LINE_COMMENT
                )
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
