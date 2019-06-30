from enum import Enum, auto


class Token(Enum):
    INVALID = auto()
    EOF = auto()

    # identifier
    IDENTIFIER = auto()

    # comments
    SINGLE_LINE_COMMENT = auto()
    MULTI_LINE_COMMENT = auto()

    # literals
    CHARACTER_CONSTANT = auto()
    INTEGER_CONSTANT = auto()
    FLOATING_CONSTANT = auto()
    STRING_CONSTANT = auto()

    # punctuators
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    DOT = auto()
    SEMICOLON = auto()
    COMMA = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_THAN_EQUALS = auto()
    GREATER_THAN_EQUALS = auto()
    EQUALS_EQUALS = auto()
    EXCLAMATION_EQUALS = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    PLUS_PLUS = auto()
    MINUS_MINUS = auto()
    LESS_THAN_LESS_THAN = auto()
    GREATER_THAN_GREATER_THAN = auto()
    AMPERSAND = auto()
    PIPE = auto()
    CARET = auto()
    EXCLAMATION = auto()
    TILDE = auto()
    AMPERSAND_AMPERSAND = auto()
    PIPE_PIPE = auto()
    QUESTION = auto()
    COLON = auto()
    ARROW = auto()

    # assignments
    EQUALS = auto()
    PLUS_EQUALS = auto()
    MINUS_EQUALS = auto()
    STAR_EQUALS = auto()
    SLASH_EQUALS = auto()
    PERCENT_EQUALS = auto()
    LESS_THAN_LESS_THAN_EQUALS = auto()
    GREATER_THAN_GREATER_THAN_EQUALS = auto()
    AMPERSAND_EQUALS = auto()
    PIPE_EQUALS = auto()
    CARET_EQUALS = auto()

    # keywords
    BREAK = auto()
    CASE = auto()
    CHAR = auto()
    CONTINUE = auto()
    DEFAULT = auto()
    DO = auto()
    ELSE = auto()
    ENUM = auto()
    IF = auto()
    INT = auto()
    LONG = auto()
    RESTRICT = auto()
    RETURN = auto()
    SHORT = auto()
    SIZEOF = auto()
    SWITCH = auto()
    TYPEDEF = auto()
    UNSIGNED = auto()
    VOID = auto()
    WHILE = auto()


KEYWORDS = {
    "break": Token.BREAK,
    "case": Token.CASE,
    "char": Token.CHAR,
    "continue": Token.CONTINUE,
    "default": Token.DEFAULT,
    "do": Token.DO,
    "else": Token.ELSE,
    "enum": Token.ENUM,
    "if": Token.IF,
    "int": Token.INT,
    "long": Token.LONG,
    "restrict": Token.RESTRICT,
    "return": Token.RETURN,
    "short": Token.SHORT,
    "sizeof": Token.SIZEOF,
    "switch": Token.SWITCH,
    "typedef": Token.TYPEDEF,
    "unsigned": Token.UNSIGNED,
    "void": Token.VOID,
    "while": Token.WHILE,
}
