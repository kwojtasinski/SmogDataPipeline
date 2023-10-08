import argparse

from smog_data_pipeline.pipelines import SmogPipeline


def prepare_parser():
    parser = argparse.ArgumentParser(
        prog="smog_data_pipeline",
        description="Pipeline for processing SMOG data using data from 'https://public-esa.ose.gov.pl'",
    )
    parser.add_argument(
        "-p",
        "--path",
        nargs=1,
        type=str,
        help="Path to save the CSV data to",
        required=True,
    )
    parser.add_argument(
        "-c", "--cache", nargs="?", type=str, help="Path to load the cache data from"
    )
    return parser


def run_pipeline(path: str, cache: str) -> None:
    pipeline = SmogPipeline(result_file_path=path, cache_path=cache)
    pipeline.run()
