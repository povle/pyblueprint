import pandas


def output_csv(data: pandas.DataFrame, path: str) -> pandas.DataFrame:
    """*.csv"""
    data.to_csv(path, index=False)
    return True
