import typing


def sum(a: int, b: int) -> int:
    return a + b


def power(a: int, b: int) -> int:
    return typing.cast(int, pow(a, b))
