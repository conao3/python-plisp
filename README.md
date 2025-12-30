# plisp

A Pure Lisp interpreter written in Python.

This project implements the original Lisp primitives as defined by John McCarthy, providing a minimal yet complete Lisp environment for learning and experimentation.

## Features

- Core Lisp primitives: `atom`, `eq`, `car`, `cdr`, `cons`, `cond`, `quote`
- Lambda expressions and function definitions
- Interactive REPL with command history
- File-based script execution
- Clean, readable implementation using Python dataclasses

## Installation

```bash
pip install plisp
```

Or install from source:

```bash
git clone https://github.com/conao3/python-plisp.git
cd python-plisp
pip install .
```

## Usage

### Interactive REPL

Start the interactive interpreter:

```bash
plisp
```

Example session:

```lisp
plisp> (car '(a b c))
a
plisp> (cdr '(a b c))
(b c)
plisp> (cons 'x '(y z))
(x y z)
plisp> (define square (lambda (x) (cons x x)))
(lambda (x) (cons x x))
plisp> (square 'a)
(a . a)
```

### Execute a File

Run a Lisp script from a file:

```bash
plisp -i script.lisp
```

Read from standard input:

```bash
echo "(car '(hello world))" | plisp -i -
```

### Debug Mode

Enable debug mode for detailed error traces:

```bash
plisp --debug
```

## Built-in Functions

| Function | Description |
|----------|-------------|
| `atom`   | Returns `t` if the argument is an atom, `nil` otherwise |
| `eq`     | Returns `t` if two atoms are equal |
| `car`    | Returns the first element of a cons cell |
| `cdr`    | Returns the rest of a cons cell |
| `cons`   | Constructs a new cons cell |
| `cond`   | Conditional expression |
| `quote`  | Returns the argument unevaluated |
| `lambda` | Creates an anonymous function |
| `define` | Binds a value to a symbol |
| `print`  | Prints a value and returns it |

## Development

Install development dependencies:

```bash
poetry install
```

Run tests:

```bash
poetry run pytest
```

## Requirements

- Python 3.10 or higher

## License

MIT
