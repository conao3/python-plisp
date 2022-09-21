from __future__ import annotations
import builtins

from . import types
from . import lib
from . import core


def atom(args: types.Expression, _env: core.Env) -> types.Symbol:
    (x,) = lib.extract_list(args)

    val = core.eval(x, _env)

    if isinstance(val, types.Atom):
        return types.T

    return types.NIL


def eq(args: types.Expression, _env: core.Env) -> types.Symbol:
    (x, y) = lib.extract_list(args, 2)

    x_val = core.eval(x, _env)
    y_val = core.eval(y, _env)

    if x_val == y_val:
        return types.T

    return types.NIL


def car(args: types.Expression, _env: core.Env) -> types.Expression:
    (x,) = lib.extract_list(args)

    val = core.eval(x, _env)

    if not isinstance(val, types.Cell):
        raise types.PlispError('Expected cons cell')

    return val.car


def cdr(args: types.Expression, _env: core.Env) -> types.Expression:
    (x,) = lib.extract_list(args)

    val = core.eval(x, _env)

    if not isinstance(val, types.Cell):
        raise types.PlispError('Expected cons cell')

    return val.cdr


def cons(args: types.Expression, _env: core.Env) -> types.Cell:
    (x, y) = lib.extract_list(args, 2)

    x_val = core.eval(x, _env)
    y_val = core.eval(y, _env)

    return types.Cell(car=x_val, cdr=y_val)


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

    return types.Cell(car=types.Symbol('lasmbda'), cdr=args)


def define(args: types.Expression, env: core.Env) -> types.Expression:
    (x, y) = lib.extract_list(args, 2)

    if not isinstance(x, types.Symbol):
        raise types.PlispError('Expected symbol')

    val = core.eval(y, env)

    x.value = val
    env.symbols[x.name] = x

    return val


def print(args: types.Expression, _env: core.Env) -> types.Expression:
    (x,) = lib.extract_list(args)

    val = core.eval(x, _env)

    builtins.print(str(val))

    return val


def makunbound(args: types.Expression, env: core.Env) -> types.Expression:
    (x,) = lib.extract_list(args)

    x_val = core.eval(x, env)

    if not isinstance(x_val, types.Symbol):
        raise types.PlispError('Expected symbol')

    if not (e := env.find(x_val.name)):
        return x_val

    e.symbols[x_val.name].value = None

    return x_val


def one_plus(args: types.Expression, _env: core.Env) -> types.Int:
    (x,) = lib.extract_list(args)

    x_val = core.eval(x, _env)

    if not isinstance(x_val, types.Int):
        raise types.PlispError('Expected integer')

    return types.Int(value=x_val.value + 1)
