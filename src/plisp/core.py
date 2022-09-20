from __future__ import annotations

import re
import string
from typing import Optional, TypeVar

from . import types
from . import builtin


class Env:
    def __init__(
        self,
        parent: Optional['Env'] = None,
        symbols: dict[str, types.Symbol] = {}
    ):
        self.parent = parent
        self.symbols = symbols

    def find(self, name: str) -> Optional[Env]:
        if name in self.symbols:
            return self

        if self.parent:
            return self.parent.find(name)


global_env = Env()


class Reader:
    def __init__(self, src: str):
        self.src = src
        self.pos = 0

        self.lensrc = len(src)

    @property
    def char(self) -> str:
        if self.pos >= self.lensrc:
            raise types.PlispError('Unexpected EOF')

        return self.src[self.pos]

    @property
    def peek_char(self) -> str:
        return self.src[self.pos + 1]

    def skip_whitespace(self):
        while self.pos < self.lensrc and self.src[self.pos] in string.whitespace:
            self.pos += 1

    def read(self) -> types.Expression:
        self.skip_whitespace()

        if self.char == ';':
            while self.src[self.pos] != '\n':
                self.pos += 1
            return self.read()  # TODO: recursion limit?

        if self.char == '(':
            self.pos += 1

            self.skip_whitespace()

            if self.char == ')':  # type: ignore
                self.pos += 1
                return types.NIL

            # list notation
            def read_list_exp() -> types.Expression:
                self.skip_whitespace()
                if self.char == ')':
                    self.pos += 1
                    return types.NIL

                if self.char == '.':  # cons notation
                    self.pos += 1
                    ret = self.read()

                    self.skip_whitespace()
                    if self.char == ')':  # type: ignore
                        self.pos += 1
                        return ret

                    raise types.PlispError('Expected `)\' after cons cdr')

                return types.Cell(car=self.read(), cdr=read_list_exp())

            return types.Cell(car=self.read(), cdr=read_list_exp())  # TODO: recursion limit?

        if self.char == ')':
            raise types.SyntaxError('unexpected `)\'')

        if (m := re.match(r'[0-9]+', self.src[self.pos:])):
            self.pos += m.end()
            return types.Int(value=int(m.group()))

        pos = self.pos
        while self.pos < self.lensrc and self.src[self.pos] not in (string.whitespace + '()'):
            self.pos += 1

        return types.Symbol(name=self.src[pos:self.pos])


def read(x: Optional[str]) -> Optional[types.Expression]:
    if not x:
        return

    return Reader(x).read()


T = TypeVar('T', None, types.Expression)
def eval(x: T, env: Env = global_env) -> T:
    if x is None:
        return x

    if isinstance(x, types.Symbol):
        if not (e := env.find(x.name)):
            raise types.PlispError(f'Undefined symbol {x.name}')

        if not (ret := e.symbols[x.name].value):
            raise types.PlispError(f'Undefined symbol {x.name}')

        return ret

    if not isinstance(x, types.Cell):
        return x

    if not isinstance(x.car, types.Symbol):
        raise types.PlispError('Expected symbol as function name')

    if x.car.name == 'atom': return builtin.atom(x.cdr, env)
    if x.car.name == 'eq': return builtin.eq(x.cdr, env)
    if x.car.name == 'car': return builtin.car(x.cdr, env)
    if x.car.name == 'cdr': return builtin.cdr(x.cdr, env)
    if x.car.name == 'cons': return builtin.cons(x.cdr, env)
    if x.car.name == 'cond': return builtin.cond(x.cdr, env)
    if x.car.name == 'quote': return builtin.quote(x.cdr, env)
    if x.car.name == 'lambda': return builtin.lambda_(x.cdr, env)
    if x.car.name == 'define': return builtin.define(x.cdr, env)

    raise types.PlispError(f'Unknown function {x.car.name}')  # TODO: lookup symbol


def print(x: Optional[types.Expression]) -> Optional[str]:
    if not x:
        return

    return str(x)


def rep(x: str) -> Optional[str]:
    return print(eval(read(x)))
