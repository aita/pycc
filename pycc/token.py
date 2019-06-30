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
    AUTO = auto()
    BREAK = auto()
    CASE = auto()
    CHAR = auto()
    CONST = auto()
    CONTINUE = auto()
    DEFAULT = auto()
    DO = auto()
    DOUBLE = auto()
    ELSE = auto()
    ENUM = auto()
    EXTERN = auto()
    FLOAT = auto()
    FOR = auto()
    GOTO = auto()
    IF = auto()
    INLINE = auto()
    INT = auto()
    LONG = auto()
    REGISTER = auto()
    RESTRICT = auto()
    RETURN = auto()
    SHORT = auto()
    SIGNED = auto()
    SIZEOF = auto()
    STATIC = auto()
    STRUCT = auto()
    SWITCH = auto()
    TYPEDEF = auto()
    UNION = auto()
    UNSIGNED = auto()
    VOID = auto()
    VOLATILE = auto()
    WHILE = auto()
    ALIGNAS = auto()
    ALIGNOF = auto()
    ATOMIC = auto()
    BOOL = auto()
    COMPLEX = auto()
    GENERIC = auto()
    IMAGINARY = auto()
    NORETURN = auto()
    STATIC_ASSERT = auto()
    THREAD_LOCAL = auto()


KEYWORDS = {
    "auto": Token.AUTO,
    "break": Token.BREAK,
    "case": Token.CASE,
    "char": Token.CHAR,
    "const": Token.CONST,
    "continue": Token.CONTINUE,
    "default": Token.DEFAULT,
    "do": Token.DO,
    "double": Token.DOUBLE,
    "else": Token.ELSE,
    "enum": Token.ENUM,
    "extern": Token.EXTERN,
    "float": Token.FLOAT,
    "for": Token.FOR,
    "goto": Token.GOTO,
    "if": Token.IF,
    "inline": Token.INLINE,
    "int": Token.INT,
    "long": Token.LONG,
    "register": Token.REGISTER,
    "restrict": Token.RESTRICT,
    "return": Token.RETURN,
    "short": Token.SHORT,
    "signed": Token.SIGNED,
    "sizeof": Token.SIZEOF,
    "struct": Token.STRUCT,
    "switch": Token.SWITCH,
    "typedef": Token.TYPEDEF,
    "union": Token.UNION,
    "unsigned": Token.UNSIGNED,
    "void": Token.VOID,
    "volatile": Token.VOLATILE,
    "while": Token.WHILE,
    "_Alignas": Token.ALIGNAS,
    "_Alignof": Token.ALIGNOF,
    "_Atomic": Token.ATOMIC,
    "_Bool": Token.BOOL,
    "_Complex": Token.COMPLEX,
    "_Generic": Token.GENERIC,
    "_Imaginary": Token.IMAGINARY,
    "_Noreturn": Token.NORETURN,
    "_Static_assert": Token.STATIC_ASSERT,
    "_Thread_local": Token.THREAD_LOCAL,
}
