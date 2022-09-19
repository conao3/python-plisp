import re
import string
from typing import Optional, TypeVar

from . import types


class Environment:
    def __init__(
        self,
        parent: Optional['Environment'] = None,
        symbols: dict[str, types.Expression] = {}
    ):
        self.parent = parent
        self.symbols = symbols


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

            if self.char == ')':
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
                    if self.char == ')':
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


T = TypeVar('T', type(None), types.Expression)
def eval(x: T) -> T:
    if not x:
        return None

    match x:
        case types.Int():
            return x

        case types.Symbol():
            return x  # TODO: lookup symbol

        case types.Cell():
            return x  # TODO: eval list

        case _:
            raise types.EvalError(f'Unknown expression type: {x}')



def print(x: Optional[types.Expression]) -> Optional[str]:
    if not x:
        return

    return str(x)


def rep(x: str) -> Optional[str]:
    return print(eval(read(x)))
