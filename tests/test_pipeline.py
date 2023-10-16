from tempfile import NamedTemporaryFile

import polars as pl
import pytest

from smog_data_pipeline.pipelines.smog import SmogPipeline


@pytest.mark.vcr("cassettes/test_smog_pipeline.yaml")
def test_smog_pipeline():
    with NamedTemporaryFile() as f:
        pipeline = SmogPipeline(result_file_path=f.name)
        pipeline.run()

        loaded_df = pl.read_csv(f.name)

        assert loaded_df.shape == (1428, 12), "Expected 1428 rows and 12 columns"
        assert loaded_df.schema == {
            "name": pl.Utf8,
            "post_code": pl.Utf8,
            "city": pl.Utf8,
            "longitude": pl.Float64,
            "latitude": pl.Utf8,
            "street": pl.Utf8,
            "humidity_avg": pl.Float64,
            "pressure_avg": pl.Float64,
            "temperature_avg": pl.Float64,
            "pm10_avg": pl.Float64,
            "pm25_avg": pl.Float64,
            "timestamp": pl.Utf8,
        }, "Expected schema to match"
