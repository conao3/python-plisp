from __future__ import annotations
import json

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

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Symbol(name={repr(self.name)}, value={repr(self.value)})'


NIL = Symbol('nil')
T = Symbol('t')


@dataclasses.dataclass
class Int(Atom):
    value: int

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f'Int(value={repr(self.value)})'


@dataclasses.dataclass
class Cell(Expression):
    car: Expression
    cdr: Expression

    def __str__(self) -> str:
        lst = []
        cell = self
        while isinstance(cell, Cell):
            lst.append(str(cell.car))
            cell = cell.cdr

        if cell == NIL:
            return '(' + ' '.join(lst) + ')'

        return '(' + ' '.join(lst) + ' . ' + str(cell) + ')'

    def __repr__(self) -> str:
        return f'Cell(car={repr(self.car)}, cdr={repr(self.cdr)})'



class PlispError(Exception):
    def __str__(self) -> str:
        name = util.camel_to_kebab(self.__class__.__name__)

        return f'({name} {" ".join([json.dumps(elm, default=str) for elm in self.args])})'


class SyntaxError(PlispError):
    pass


class EvalError(PlispError):
    pass


class WrongTypeArgument(PlispError):
    pass


class WrongNumberOfArguments(PlispError):
    pass


class VoidValiable(PlispError):
    pass
