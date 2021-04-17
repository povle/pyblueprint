import pandas


def bypass(data: pandas.DataFrame) -> pandas.DataFrame:
    return data


def transpose(data: pandas.DataFrame) -> pandas.DataFrame:
    return data.transpose()


def scale(data: pandas.DataFrame, factor: int) -> pandas.DataFrame:
    return data * factor


def pow(data: pandas.DataFrame, power: int) -> pandas.DataFrame:
    return data.applymap(lambda x: x**power)
