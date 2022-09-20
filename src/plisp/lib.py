from typing import TypeGuard
import typing

from . import types


def listp(exp: types.Expression) -> TypeGuard[types.Cell]:
    if not isinstance(exp, types.Cell):
        return False

    return True


def extract_list(arg: types.Expression, num: int = 1) -> list[types.Expression]:
    ret: list[types.Expression] = []

    if not listp(arg):
        raise types.WrongTypeArgument('listp', arg)

    for i in range(num - 1):
        ret.append(arg.car)

        if not listp(arg.cdr):
            raise types.WrongNumberOfArguments(num, i + 1)

        arg = arg.cdr

    ret.append(arg.car)

    if not arg.cdr == types.NIL:
        raise types.WrongNumberOfArguments(num, num + 1)

    return ret


def cell_iter(arg: types.Expression) -> typing.Iterator[types.Expression]:
    if not listp(arg):
        return

    while listp(arg):
        yield arg.car
        arg = arg.cdr

    if arg != types.NIL:
        raise types.WrongTypeArgument('listp', arg)
