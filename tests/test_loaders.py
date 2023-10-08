import polars as pl
from tempfile import NamedTemporaryFile

from smog_data_pipeline.loaders import CSVLoader


def test_csv_loader():
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    with NamedTemporaryFile() as f:
        loader = CSVLoader(path=f.name)
        loader.load(df)
        loaded_df = pl.read_csv(f.name)

        assert loaded_df.shape == (3, 2)
        assert loaded_df.columns == ["a", "b"]
