import polars as pl

from smog_data_pipeline.transformers import (
    CastTransformer,
    DropTransformer,
    ExplodeTransformer,
    StripStringTransformer,
    UnnestTransformer,
)


def test_drop_transformer():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    transformer = DropTransformer(columns=["a"])

    result_df = transformer(df)

    assert result_df.shape == (3, 1)
    assert result_df.columns == ["b"]


def test_explode_transformer():
    df = pl.DataFrame({"a": [[1, 2, 3], [4, 5, 6]]})
    transformer = ExplodeTransformer(column="a")

    result_df = transformer(df)

    assert result_df.shape == (6, 1)
    assert result_df.columns == ["a"]


def test_unnest_transformer():
    df = pl.DataFrame({"a": [{"b": 1}, {"b": 2}]})
    transformer = UnnestTransformer(column="a")

    result_df = transformer(df)

    assert result_df.shape == (2, 1)
    assert result_df.columns == ["b"]


def test_cast_transformer():
    df = pl.DataFrame({"a": ["1", "2", "3"]})
    transformer = CastTransformer(column="a", dtype=pl.Int8)

    result_df = transformer(df)

    assert result_df.shape == (3, 1)
    assert result_df.columns == ["a"]
    assert result_df.dtypes == [pl.Int8]
    assert result_df.frame_equal(pl.DataFrame({"a": [1, 2, 3]}))


def test_strip_string_transformer():
    df = pl.DataFrame({"a": [" 1 ", " 2 ", " 3 "]})
    transformer = StripStringTransformer(column="a")

    result_df = transformer(df)

    assert result_df.shape == (3, 1)
    assert result_df.columns == ["a"]
    assert result_df.frame_equal(pl.DataFrame({"a": ["1", "2", "3"]}))
