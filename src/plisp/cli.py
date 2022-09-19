import argparse
import readline
import sys
from typing import Optional


def read(x: Optional[str]) -> Optional[str]:
    return x


def eval(x: Optional[str]) -> Optional[str]:
    return x


def print(x: Optional[str]) -> Optional[str]:
    return x


def rep(x: Optional[str]) -> Optional[str]:
    return print(eval(read(x)))


def repl():
    while True:
        try:
            line = input("plisp> ")
            readline.add_history(line)
            print(rep(line))
        except EOFError:
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    args = parser.parse_args()


    if not args.input:
        repl()
        exit()

    infile = sys.stdin if args.input == "-" else open(args.input)

    print(rep(infile.read()))
