import logging
from typing import Optional


from smog_data_pipeline.extractors import HttpExtractor
from smog_data_pipeline.loaders import CSVLoader
from smog_data_pipeline.pipelines.base import Pipeline
from smog_data_pipeline.transformers import (
    DropTransformer,
    ExplodeTransformer,
    StripStringTransformer,
    UnnestTransformer,
)

logger = logging.getLogger(__name__)


class SmogPipeline(Pipeline):
    def __init__(self, result_file_path: str, cache_path: Optional[str] = None) -> None:
        transformers = [
            DropTransformer(columns=["it_has_next_page"]),
            ExplodeTransformer(column="smog_data"),
            UnnestTransformer(column="smog_data"),
            UnnestTransformer(column="school"),
            UnnestTransformer(column="data"),
            StripStringTransformer(column="longitude"),
        ]
        extractor = HttpExtractor(
            url="https://public-esa.ose.gov.pl/api/v1/smog",
            method="GET",
            cache_path=cache_path,
        )
        loader = CSVLoader(path=result_file_path)
        super().__init__(extractor=extractor, transformers=transformers, loader=loader)
