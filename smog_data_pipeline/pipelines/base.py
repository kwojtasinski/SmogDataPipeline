import logging
import time

import polars as pl

from smog_data_pipeline.extractors import Extractor
from smog_data_pipeline.loaders import Loader
from smog_data_pipeline.transformers import (
    Transformer,
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
            logger.info(
                "Transformed data using %s (attributes=%s)",
                transformer.__class__.__name__,
                transformer.get_attributes(),
            )
        logger.info("Head of the data:\n%s", data.head(5))
        self.loader.load(data)
        logger.info(
            "Pipeline finished in %s seconds", round(time.time() - start_time, 2)
        )

    def __call__(self) -> pl.DataFrame:
        return self.run()
