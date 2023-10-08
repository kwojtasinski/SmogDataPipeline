import logging
import time
from typing import Optional

import polars as pl

from smog_data_pipeline.extractors import Extractor, HttpExtractor
from smog_data_pipeline.loaders import CSVLoader, Loader
from smog_data_pipeline.transformers import (
    DropTransformer,
    ExplodeTransformer,
    Transformer,
    UnnestTransformer,
)

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(
        self, extractor: Extractor, transformers: list[Transformer], loader: Loader
    ) -> None:
        self.extractor = extractor
        self.transformers = transformers
        self.loader = loader

    def run(self) -> None:
        start_time = time.time()
        data = self.extractor.extract()
        for transformer in self.transformers:
            data = transformer.transform(data)
            logger.info("Transformed data using %s", transformer.__class__.__name__)
        self.loader.load(data)
        logger.info("Pipeline finished in %s seconds", time.time() - start_time)

    def __call__(self) -> pl.DataFrame:
        return self.run()


class SmogPipeline(Pipeline):
    def __init__(self, result_file_path: str, cache_path: Optional[str] = None) -> None:
        transformers = [
            DropTransformer(columns=["it_has_next_page"]),
            ExplodeTransformer(column="smog_data"),
            UnnestTransformer(column="smog_data"),
            UnnestTransformer(column="school"),
            UnnestTransformer(column="data"),
        ]
        extractor = HttpExtractor(
            url="https://public-esa.ose.gov.pl/api/v1/smog",
            method="GET",
            cache_path=cache_path,
        )
        loader = CSVLoader(path=result_file_path)
        super().__init__(extractor=extractor, transformers=transformers, loader=loader)
