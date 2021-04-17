import pandas


def plot_dataframe(data: pandas.DataFrame, axes) -> pandas.DataFrame:
    data.plot(ax=axes)
    return True
