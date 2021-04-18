import pandas


def input_csv(path: str) -> pandas.DataFrame:
    """*.csv"""
    return pandas.read_csv(path)
