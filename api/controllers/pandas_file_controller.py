import pandas as pd
from pandas import DataFrame


class PandasDf:
    @staticmethod
    def read_csv(path: str) -> DataFrame:
        df = pd.read_csv(path)
        return df

    @staticmethod
    def write_csv(path: str, df: DataFrame, index: bool = False):
        df.to_csv(path, index=index)
