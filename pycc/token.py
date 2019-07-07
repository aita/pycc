from enum import Enum


class Token(Enum):
    INVALID = "invalid token"
    EOF = "eof"

    # identifier
    IDENTIFIER = "identifier"

    # comments
    SINGLE_LINE_COMMENT = "// comment"
    MULTI_LINE_COMMENT = "/* comment"

    # literals
    CHARACTER_CONSTANT = "character constant"
    INTEGER_CONSTANT = "integer constant"
    FLOATING_CONSTANT = "floating constant"
    STRING_CONSTANT = "string constant"

    # punctuators
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    PERIOD = "."
    ELLIPSIS = "..."
    SEMICOLON = ";"
    COMMA = ","
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_THAN_EQUALS = "<="
    GREATER_THAN_EQUALS = ">="
    EQUALS_EQUALS = "=="
    EXCLAMATION_EQUALS = "!="
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"
    PLUS_PLUS = "++"
    MINUS_MINUS = "--"
    LESS_THAN_LESS_THAN = "<<"
    GREATER_THAN_GREATER_THAN = ">>"
    AMPERSAND = "&"
    PIPE = "|"
    CARET = "^"
    EXCLAMATION = "!"
    TILDE = "~"
    AMPERSAND_AMPERSAND = "&&"
    PIPE_PIPE = "||"
    QUESTION = "?"
    COLON = ":"
    ARROW = "->"
    EQUALS = "="
    PLUS_EQUALS = "+="
    MINUS_EQUALS = "-="
    STAR_EQUALS = "*="
    SLASH_EQUALS = "/="
    PERCENT_EQUALS = "%="
    LESS_THAN_LESS_THAN_EQUALS = "<<="
    GREATER_THAN_GREATER_THAN_EQUALS = ">>="
    AMPERSAND_EQUALS = "&="
    PIPE_EQUALS = "|="
    CARET_EQUALS = "^="
    HASH = "#"
    HASH_HASH = "##"

    # keywords
    AUTO = "auto"
    BREAK = "break"
    CASE = "case"
    CHAR = "char"
    CONST = "const"
    CONTINUE = "continue"
    DEFAULT = "default"
    DO = "do"
    DOUBLE = "double"
    ELSE = "else"
    ENUM = "enum"
    EXTERN = "extern"
    FLOAT = "float"
    FOR = "for"
    GOTO = "goto"
    IF = "if"
    INLINE = "inline"
    INT = "int"
    LONG = "long"
    REGISTER = "register"
    RESTRICT = "restrict"
    RETURN = "return"
    SHORT = "short"
    SIGNED = "signed"
    SIZEOF = "sizeof"
    STATIC = "static"
    STRUCT = "struct"
    SWITCH = "switch"
    TYPEDEF = "typedef"
    UNION = "union"
    UNSIGNED = "unsigned"
    VOID = "void"
    VOLATILE = "volatile"
    WHILE = "while"
    ALIGNAS = "_Alignas"
    ALIGNOF = "_Alignof"
    ATOMIC = "_Atomic"
    BOOL = "_Bool"
    COMPLEX = "_Complex"
    GENERIC = "_Generic"
    IMAGINARY = "_Imaginary"
    NORETURN = "_No_return"
    STATIC_ASSERT = "_Static_assert"
    THREAD_LOCAL = "_Thread_local"


KEYWORDS = {
    Token.AUTO,
    Token.BREAK,
    Token.CASE,
    Token.CHAR,
    Token.CONST,
    Token.CONTINUE,
    Token.DEFAULT,
    Token.DO,
    Token.DOUBLE,
    Token.ELSE,
    Token.ENUM,
    Token.EXTERN,
    Token.FLOAT,
    Token.FOR,
    Token.GOTO,
    Token.IF,
    Token.INLINE,
    Token.INT,
    Token.LONG,
    Token.REGISTER,
    Token.RESTRICT,
    Token.RETURN,
    Token.SHORT,
    Token.SIGNED,
    Token.SIZEOF,
    Token.STRUCT,
    Token.SWITCH,
    Token.TYPEDEF,
    Token.UNION,
    Token.UNSIGNED,
    Token.VOID,
    Token.VOLATILE,
    Token.WHILE,
    Token.ALIGNAS,
    Token.ALIGNOF,
    Token.ATOMIC,
    Token.BOOL,
    Token.COMPLEX,
    Token.GENERIC,
    Token.IMAGINARY,
    Token.NORETURN,
    Token.STATIC_ASSERT,
    Token.THREAD_LOCAL,
}

PUNCTUATORS = {
    Token.LEFT_BRACE,
    Token.RIGHT_BRACE,
    Token.LEFT_PAREN,
    Token.RIGHT_PAREN,
    Token.LEFT_BRACKET,
    Token.RIGHT_BRACKET,
    Token.PERIOD,
    Token.ELLIPSIS,
    Token.COMMA,
    Token.SEMICOLON,
    Token.LESS_THAN,
    Token.LESS_THAN_EQUALS,
    Token.LESS_THAN_LESS_THAN,
    Token.LESS_THAN_LESS_THAN_EQUALS,
    Token.GREATER_THAN,
    Token.GREATER_THAN_EQUALS,
    Token.GREATER_THAN_GREATER_THAN,
    Token.GREATER_THAN_GREATER_THAN_EQUALS,
    Token.EQUALS,
    Token.EQUALS_EQUALS,
    Token.EXCLAMATION,
    Token.EXCLAMATION_EQUALS,
    Token.PLUS,
    Token.PLUS_PLUS,
    Token.PLUS_EQUALS,
    Token.MINUS,
    Token.MINUS_MINUS,
    Token.MINUS_EQUALS,
    Token.ARROW,
    Token.STAR,
    Token.STAR_EQUALS,
    Token.SLASH,
    Token.SLASH_EQUALS,
    Token.PERCENT,
    Token.PERCENT_EQUALS,
    Token.AMPERSAND,
    Token.AMPERSAND_AMPERSAND,
    Token.AMPERSAND_EQUALS,
    Token.PIPE,
    Token.PIPE_PIPE,
    Token.PIPE_EQUALS,
    Token.CARET,
    Token.CARET_EQUALS,
    Token.TILDE,
    Token.QUESTION,
    Token.COLON,
    Token.HASH,
    Token.HASH_HASH,
}
