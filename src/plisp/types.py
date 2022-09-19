from __future__ import annotations

from typing import Optional
import dataclasses

from . import util


class Expression:
    pass


class Atom(Expression):
    pass


@dataclasses.dataclass
class Symbol(Atom):
    name: str
    value: Optional[Expression] = None
    function: Optional[Expression] = None

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Symbol(name={repr(self.name)}, value={repr(self.value)}, function={repr(self.function)})'


@dataclasses.dataclass
class Int(Atom):
    value: int

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f'Int(value={repr(self.value)})'


@dataclasses.dataclass
class Cell(Expression):
    car: Optional[Expression] = None
    cdr: Optional[Expression] = None

    def __str__(self) -> str:
        return f'({self.car} . {self.cdr})'

    def __repr__(self) -> str:
        return f'Cell(car={repr(self.car)}, cdr={repr(self.cdr)})'



class PlispError(Exception):
    def __str__(self) -> str:
        return f'({util.camel_to_kebab(self.__class__.__name__)} "{self.args[0]}")'


class SyntaxError(PlispError):
    pass
