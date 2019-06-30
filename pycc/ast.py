import dataclasses
from .file import Location


@dataclasses.dataclass
class IntegerConstant:
    location: Location
    text: str
    value: int


@dataclasses.dataclass
class FloatingConstant:
    location: Location
    text: str
    value: float


@dataclasses.dataclass
class StringConstant:
    location: Location
    text: str
    value: str


@dataclasses.dataclass
class CharacterConstant:
    location: Location
    text: str
    value: str

