import dataclasses
from enum import Enum
from typing import Union

from .file import Location


class Error(Enum):
    UNKNOWN_CHARACTER = "unknown character"
    UNTERMINATED_MULTI_LINE_COMMENT = "unterminated /* comment"
    UNTERMINATED_STRING = "unterminated string"
    UNTERMINATED_CHARACTER = "unterminated character"
    INVALID_INTEGER_CONSTANT_SUFFIX = "invalid integer constant suffix"
    INVALID_FLOATING_CONSTANT_SUFFIX = "invalid floating constant suffix"
    INVALID_DIGIT = "invalid digit"
    INVALID_FLOATING_EXPONENT = "invalid floating exponent"
    INVALID_ESCAPE_SEQUENCE = "invalid escape sequence"


class Warning(Enum):
    UNKNOWN_ESCAPE_SEQUENCE = "unknown escape sequence"


@dataclasses.dataclass
class ErrorInfo:
    location: Location
    name: Union[Error, Warning]
    message: str
