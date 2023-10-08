from abc import ABC, abstractmethod
import logging
from pathlib import Path
from typing import Optional

import polars as pl
import requests

logger = logging.getLogger(__name__)


class Extractor(ABC):
    @abstractmethod
    def extract(self) -> pl.DataFrame:
        pass


class HttpExtractor(Extractor):
    def _make_request(self) -> requests.Response:
        response = requests.request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            params=self.params,
            data=self.payload,
        )
        response.raise_for_status()
        logger.info("Made %s request to %s", self.method, self.url)
        return response

    def __init__(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        payload: Optional[dict] = None,
        cache_path: Optional[str] = None,
    ):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.payload = payload
        self.cache_path = cache_path

        if self.cache_path is not None:
            path = Path(self.cache_path)
            if path.exists():
                logger.info("Reading data from cache: %s", self.cache_path)
                self.data = path.read_bytes()
            else:
                self.data = self._make_request().content
                path.write_bytes(self.data)
        else:
            self.data = self._make_request().content

    def extract(self) -> pl.DataFrame:
        return pl.read_json(self.data)
