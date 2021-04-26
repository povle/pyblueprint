import sqlite3
from pandas import DataFrame


def output_csv(data: DataFrame, path: str) -> DataFrame:
    """*.csv"""
    data.to_csv(path, index=False)
    return True


def output_xlsx(data: DataFrame, path: str) -> DataFrame:
    """*.xlsx"""
    data.to_excel(path, index=False)
    return True


def output_sqlite(data: DataFrame, path: str, table_name: str) -> DataFrame:
    """*.sqlite3 *.sqlite *.db"""
    name = table_name or 'data'
    with sqlite3.connect(path) as conn:
        data.to_sql(name, conn, if_exists='replace')
