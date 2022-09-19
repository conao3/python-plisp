import re


pat_camel = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_kebab(name):
    return pat_camel.sub('-', name).lower()


def camel_to_snake(name):
    return pat_camel.sub('_', name).lower()
