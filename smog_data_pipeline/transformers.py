from abc import ABC, abstractmethod

import polars as pl


class Transformer(ABC):
    @abstractmethod
    def transform(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        pass

    def __call__(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        return self.transform(dataframe=dataframe)


class ExplodeTransformer(Transformer):
    def __init__(self, column: str) -> None:
        self.column = column

    def transform(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        return dataframe.explode(self.column)


class UnnestTransformer(Transformer):
    def __init__(self, column: str) -> None:
        self.column = column

    def transform(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        return dataframe.unnest(self.column)


class DropTransformer(Transformer):
    def __init__(self, columns: list[str]) -> None:
        self.columns = columns

    def transform(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        return dataframe.drop(self.columns)


class CastTransformer(Transformer):
    def __init__(self, column: str, dtype: str) -> None:
        self.column = column
        self.dtype = dtype

    def transform(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        return dataframe.with_column(
            self.column, dataframe[self.column].cast(self.dtype)
        )
