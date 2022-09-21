from plisp import core


def test__001_read():
    with open('./tests/specs/001_read.lisp', 'r') as f:
        ret = None
        env = core.Env()

        for line in f:
            line = line.strip()

            if line.startswith(';;') or line.startswith(';>>>'):
                continue

            if line.startswith(';'):
                assert ret == line[len(';=>'):]
                continue

            if line:
                print(repr(line))
                ret = str(core.read(line))
