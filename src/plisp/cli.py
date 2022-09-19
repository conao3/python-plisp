import argparse
import builtins
import re
import readline
import string
import sys
from typing import Optional

from . import types


class Reader:
    def __init__(self, src: str):
        self.src = src
        self.pos = 0

        self.lensrc = len(src)

    @property
    def char(self) -> str:
        return self.src[self.pos]

    @property
    def peek_char(self) -> str:
        return self.src[self.pos + 1]

    def read(self) -> types.Expression:
        # breakpoint()
        if self.char in string.whitespace:
            while self.pos < self.lensrc and self.char in string.whitespace:
                self.pos += 1

        if self.char == ';':
            while self.src[self.pos] != '\n':
                self.pos += 1
            return self.read()  # TODO: recursion limit?

        if self.char == '(':
            return  # TODO: read list

        if self.char == ')':
            raise types.SyntaxError('Unbalanced parentheses')

        if (m := re.match(r'[0-9]+', self.src[self.pos:])):
            self.pos = m.end()
            return types.Int(value=int(m.group()))

        pos = self.pos
        while self.pos < self.lensrc and self.src[self.pos] not in string.whitespace:
            self.pos += 1

        return types.Symbol(name=self.src[pos:self.pos])


def read(x: Optional[str]) -> Optional[types.Expression]:
    if not x:
        return

    return Reader(x).read()


def eval(x: Optional[types.Expression]) -> Optional[types.Expression]:
    return x


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
