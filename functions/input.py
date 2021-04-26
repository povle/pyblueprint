import sqlite3
import pandas


def input_csv(path: str) -> pandas.DataFrame:
    """*.csv"""
    return pandas.read_csv(path)


def input_xlsx(path: str) -> pandas.DataFrame:
    """*.xlsx"""
    return pandas.read_excel(path)


def input_sqlite(path: str, table_name: str) -> pandas.DataFrame:
    """*.sqlite3 *.sqlite *.db"""
    name = table_name or 'data'
    with sqlite3.connect(path) as conn:
        return pandas.read_sql(f'select * from {name}', conn)
