import pandas
from matplotlib.axes import Axes


def plot_df(data: pandas.DataFrame, axes: Axes) -> pandas.DataFrame:
    """Построить график DataFrame"""
    data.plot(ax=axes)
    return True


def table_df(data: pandas.DataFrame, axes: Axes) -> pandas.DataFrame:
    """Построить таблицу DataFrame"""
    axes.axis('off')
    axes.axis('tight')
    axes.table(cellText=data.values, colLabels=data.columns, loc='center')
    return True
