import dataclasses

from .file import Location


@dataclasses.dataclass
class Node:
    start: Location
    end: Location


class Expr(Node):
    pass


@dataclasses.dataclass
class IntegerConstant(Expr):
    text: str
    value: int


@dataclasses.dataclass
class FloatingConstant(Expr):
    start: Location
    end: Location
    text: str
    value: float


@dataclasses.dataclass
class StringConstant(Expr):
    text: str
    value: str


@dataclasses.dataclass
class CharacterConstant(Expr):
    text: str
    value: str


@dataclasses.dataclass
class RefDeclExpr(Expr):
    name: str


@dataclasses.dataclass
class ParenExpr(Expr):
    expr: Expr


class Stmt(Node):
    pass


@dataclasses.dataclass
class ExprStmt(Stmt):
    expr: Expr


@dataclasses.dataclass
class TranslationUnit(Node):
    pass
