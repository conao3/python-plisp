from __future__ import annotations

import re
import string
import typing
from typing import Optional

from . import types
from . import builtin
from . import lib


class Env:
    def __init__(
        self,
        symbols: dict[str, types.Symbol] = {},
        parent: Optional['Env'] = None,
    ):
        self.parent = parent
        self.symbols = symbols

    def find(self, name: str) -> Optional[Env]:
        if name in self.symbols:
            return self

        if self.parent:
            return self.parent.find(name)


builtin_functions = {
    'atom': types.BuiltinFunction(name='atom', value=builtin.atom),
    'eq': types.BuiltinFunction(name='eq', value=builtin.eq),
    'car': types.BuiltinFunction(name='car', value=builtin.car),
    'cdr': types.BuiltinFunction(name='cdr', value=builtin.cdr),
    'cons': types.BuiltinFunction(name='cons', value=builtin.cons),
    'cond': types.BuiltinFunction(name='cond', value=builtin.cond),
    'quote': types.BuiltinFunction(name='quote', value=builtin.quote),
    'lambda': types.BuiltinFunction(name='lambda', value=builtin.lambda_),
    'define': types.BuiltinFunction(name='define', value=builtin.define),
    'print': types.BuiltinFunction(name='print', value=builtin.print),

    # out of scope of Pure Lisp
    'makunbound': types.BuiltinFunction(name='makunbound', value=builtin.makunbound),
    '1+': types.BuiltinFunction(name='1+', value=builtin.one_plus),
}


def create_env() -> Env:
    return Env(symbols={elm: types.Symbol(name=elm, value=fn) for elm, fn in builtin_functions.items()})


global_env = create_env()


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

        if self.char == "'":
            self.pos += 1
            body = types.Cell(car=self.read(), cdr=types.NIL)
            return types.Cell(car=types.Symbol('quote'), cdr=body)

        if self.char == ':':
            pos = self.pos
            while self.pos < self.lensrc and self.src[self.pos] not in (string.whitespace + '()'):
                self.pos += 1

            return types.Symbol(name=self.src[pos:self.pos])

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

        if (m := re.match(r'[+-]?[0-9]+(?=[ ();])', self.src[self.pos:])):
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


def lambda_apply(proc: types.Expression, raw_cdr: types.Expression, env: Env) -> types.Expression:
    if not isinstance(proc, types.Cell):
        raise types.PlispError(f'Expected function, got {proc}')

    args = [eval(elm, env) for elm in lib.cell_iter(raw_cdr)]

    if (
        (proc is None) or
        (not lib.listp(proc)) or
        (not isinstance(proc.car, types.Symbol)) or
        (proc.car.name != 'lambda')
    ):
        raise types.PlispError(f'Expected lambda, got {proc}')

    (params, body) = lib.extract_list(proc.cdr, 2)

    params_lst = list(lib.cell_iter(params))
    if not all(isinstance(elm, types.Symbol) for elm in params_lst):
        raise types.PlispError(f'Expected list of symbols, got {params}')

    params_syms = typing.cast(list[types.Symbol], params_lst)
    fn_symbols = {
        param.name: types.Symbol(name=param.name, value=value)
        for param, value in zip(params_syms, args)
    }

    return eval(body, Env(env.symbols | fn_symbols, env))


@typing.overload
def eval(x: None, env: Env) -> None: ...

@typing.overload
def eval(x: types.Expression, env: Env) -> types.Expression: ...

def eval(x: Optional[types.Expression], env: Env = global_env):
    if not x:
        return

    if isinstance(x, types.Symbol):
        if x.name == 'nil': return types.NIL
        if x.name == 't': return types.T
        if x.name.startswith(':'): return x

        if (
            (not (e := env.find(x.name))) or
            (not (ret := e.symbols[x.name].value))
        ):
            raise types.PlispError(f'Undefined symbol {x.name}')

        return ret

    if not isinstance(x, types.Cell):
        return x

    proc = eval(x.car, env)

    if isinstance(proc, types.Symbol):
        proc = eval(proc, env)

    if isinstance(proc, types.BuiltinFunction):
        return proc.value(x.cdr, env)

    return lambda_apply(proc, x.cdr, env)


def print(x: Optional[types.Expression]) -> Optional[str]:
    if not x:
        return

    return str(x)


def rep(x: str) -> Optional[str]:
    return print(eval(read(x)))  # type: ignore
