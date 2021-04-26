import pandas


def transpose(data: pandas.DataFrame) -> pandas.DataFrame:
    """Транспонировать DataFrame"""
    return data.transpose()


def scale(data: pandas.DataFrame, factor: float) -> pandas.DataFrame:
    """Умножить каждый элемент DataFrame на factor"""
    return data * factor


def pow(data: pandas.DataFrame, power: int) -> pandas.DataFrame:
    """Возвести каждый элемент DataFrame в степень power"""
    return data.applymap(lambda x: x**power)
