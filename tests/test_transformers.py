import polars as pl

from smog_data_pipeline.transformers import (
    DropTransformer,
    ExplodeTransformer,
    UnnestTransformer,
)


def test_drop_transformer():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    transformer = DropTransformer(columns=["a"])
    assert transformer(df).shape == (3, 1)
    assert transformer(df).columns == ["b"]


def test_explode_transformer():
    df = pl.DataFrame({"a": [[1, 2, 3], [4, 5, 6]]})
    transformer = ExplodeTransformer(column="a")
    assert transformer(df).shape == (6, 1)
    assert transformer(df).columns == ["a"]


def test_unnest_transformer():
    df = pl.DataFrame({"a": [{"b": 1}, {"b": 2}]})
    transformer = UnnestTransformer(column="a")
    assert transformer(df).shape == (2, 1)
    assert transformer(df).columns == ["b"]
