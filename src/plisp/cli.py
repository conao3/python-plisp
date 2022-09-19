import argparse
import logging
import readline
import sys

from . import types
from . import core


logger = logging.getLogger(__name__)


def repl():
    while True:
        try:
            line = input("plisp> ")
            if line:
                readline.add_history(line)

            if (ret := core.rep(line)):
                print(ret)

        except types.PlispError as e:
            print(f'Error: {e}')

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

    if (ret := core.rep(infile.read())):
        print(ret)
