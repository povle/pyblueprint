import pandas


def input_csv(path: str) -> pandas.DataFrame:
    return pandas.read_csv(path)
