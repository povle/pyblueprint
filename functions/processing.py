import pandas


def transpose(data: pandas.DataFrame) -> pandas.DataFrame:
    """Транспонирует DataFrame"""
    return data.transpose()


def scale(data: pandas.DataFrame, factor: float) -> pandas.DataFrame:
    """Умножает каждый элемент DataFrame на factor"""
    return data * factor


def pow(data: pandas.DataFrame, power: int) -> pandas.DataFrame:
    """Возводит каждый элемент DataFrame в степень power"""
    return data.applymap(lambda x: x**power)
