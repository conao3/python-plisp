from __future__ import annotations

from . import types
from . import lib
from . import core


def atom(args: types.Expression, _env: core.Env) -> types.Symbol:
    (x,) = lib.extract_list(args)

    if isinstance(x, types.Atom):
        return types.T

    return types.NIL


def eq(args: types.Expression, _env: core.Env) -> types.Symbol:
    (x, y) = lib.extract_list(args, 2)

    if x == y:
        return types.T

    return types.NIL


def car(args: types.Expression, _env: core.Env) -> types.Expression:
    (x,) = lib.extract_list(args)

    if not isinstance(x, types.Cell):
        raise types.PlispError('Expected cons cell')

    return x.car


def cdr(args: types.Expression, _env: core.Env) -> types.Expression:
    (x,) = lib.extract_list(args)

    if not isinstance(x, types.Cell):
        raise types.PlispError('Expected cons cell')

    return x.cdr


def cons(args: types.Expression, _env: core.Env) -> types.Cell:
    (x, y) = lib.extract_list(args, 2)

    return types.Cell(car=x, cdr=y)


def cond(args: types.Expression, env: core.Env) -> types.Expression:
    for arg in lib.cell_iter(args):
        if not isinstance(arg, types.Cell):
            raise types.PlispError('Expected cons cell')

        if (ret := core.eval(arg.car, env)) != types.NIL:
            for x in lib.cell_iter(arg.cdr):
                ret = core.eval(x, env)

            return ret

    return types.NIL


def quote(args: types.Expression, _env: core.Env) -> types.Expression:
    (x,) = lib.extract_list(args)

    return x


def lambda_(args: types.Expression, _env: core.Env) -> types.Cell:
    (_params, _body) = lib.extract_list(args, 2)  # just check

    return types.Cell(car=types.Symbol('lambda'), cdr=args)


def define(args: types.Expression, env: core.Env) -> types.Expression:
    (x, y) = lib.extract_list(args, 2)

    if not isinstance(x, types.Symbol):
        raise types.PlispError('Expected symbol')

    x.value = (val := core.eval(y, env))
    env.symbols[x.name] = x

    return val
