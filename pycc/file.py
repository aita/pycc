import dataclasses


@dataclasses.dataclass
class File:
    filename: str
    source: str

    @classmethod
    def open(cls, filename: str) -> "File":
        with open(filename, newline="") as fp:
            return File(filename, fp.read())


@dataclasses.dataclass
class Location:
    filename: str
    pos: int
    line: int
    column: int
