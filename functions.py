from typing import Union


def bypass(data: str) -> str:
    return data


def reverse(data: str) -> str:
    return data[::-1]


def capitalize(data: str) -> str:
    return data.upper()


def to_int(data: str) -> int:
    return int(data)


def to_str(data: Union[str, int]) -> str:
    return str(data)


def square(data: int) -> int:
    return data**2


def to_hex(data: int, capitalize: bool, offset: int) -> str:
    h = hex(data+offset)
    if capitalize:
        h = h.upper()
    return h
