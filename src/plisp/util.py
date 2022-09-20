import re


pat_camel = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_kebab(arg: str) -> str:
    return pat_camel.sub('-', arg).lower()


def camel_to_snake(arg: str) -> str:
    return pat_camel.sub('_', arg).lower()
