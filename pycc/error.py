import dataclasses
from enum import Enum
from typing import List, Tuple, Optional
import logging

from .file import Location

logger = logging.getLogger("pycc." + __name__)


class Error(Enum):
    # scan error
    UNKNOWN_CHARACTER = "unknown character"
    UNTERMINATED_MULTI_LINE_COMMENT = "unterminated /* comment"
    UNTERMINATED_STRING = "unterminated string"
    UNTERMINATED_CHARACTER = "unterminated character"
    INVALID_INTEGER_CONSTANT_SUFFIX = "invalid integer constant suffix"
    INVALID_FLOATING_CONSTANT_SUFFIX = "invalid floating constant suffix"
    INVALID_DIGIT = "invalid digit"
    INVALID_FLOATING_EXPONENT = "invalid floating exponent"
    INVALID_ESCAPE_SEQUENCE = "invalid escape sequence"

    # parse error
    UNEXPECTED_TOKEN = "unexpected token"


class Warning(Enum):
    UNKNOWN_ESCAPE_SEQUENCE = "unknown escape sequence"


@dataclasses.dataclass
class Reporter:
    errors: List[Tuple[Location, Error]] = dataclasses.field(default_factory=list)
    warnings: List[Tuple[Location, Warning]] = dataclasses.field(default_factory=list)

    def error(
        self, location: Location, error: Error, message: Optional[str] = None
    ) -> None:
        self.errors.append((location, error))
        if message is None:
            message = error.value
        logger.error(f"{location}: {message}")

    def warning(
        self, location: Location, warning: Warning, message: Optional[str] = None
    ) -> None:
        self.warnings.append((location, warning))
        if message is None:
            message = warning.value
        logger.warning(f"{location}: {message}")
