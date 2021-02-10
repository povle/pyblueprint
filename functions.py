from typing import Union


def bypass(data: str) -> str:
    return data


def reverse(data: str) -> str:
    return data[::-1]


def capitalize(data: str) -> str:
    return data.upper()


def to_int(data: str) -> int:
    try:
        return int(data)
    except ValueError:
        return -1


def to_str(data: Union[str, int]) -> str:
    return str(data)


def square(data: int) -> int:
    return data**2


def to_hex(data: int) -> str:
    return hex(data)
