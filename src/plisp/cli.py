import argparse
import builtins
import logging
import re
import readline
import string
import sys
from typing import Optional

from . import types


logger = logging.getLogger(__name__)


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


def eval(x: Optional[types.Expression]) -> Optional[types.Expression]:
    if not x:
        return

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


def repl():
    while True:
        try:
            line = input("plisp> ")
            if line:
                readline.add_history(line)

            if (ret := rep(line)):
                builtins.print(ret)

        except types.PlispError as e:
            builtins.print(f'Error: {e}')

        except (KeyboardInterrupt, EOFError):
            break

        except Exception as e:
            logger.exception('Plisp internal error')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    args = parser.parse_args()


    if not args.input:
        repl()
        exit()

    infile = sys.stdin if args.input == "-" else open(args.input)

    if (ret := rep(infile.read())):
        builtins.print(ret)
