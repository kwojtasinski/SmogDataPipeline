from abc import ABC, abstractmethod
import logging

import polars as pl

logger = logging.getLogger(__name__)


class Loader(ABC):
    @abstractmethod
    def load(self, dataframe: pl.DataFrame) -> None:
        pass


class CSVLoader(Loader):
    def __init__(self, path: str) -> None:
        self.path = path

    def load(self, dataframe: pl.DataFrame) -> None:
        dataframe.write_csv(file=self.path)
        logger.info("Saved CSV file to %s", self.path)
