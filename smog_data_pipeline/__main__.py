from smog_data_pipeline.cli.base import prepare_parser, run_pipeline

parser = prepare_parser()
args = parser.parse_args()

run_pipeline(path=args.path[0], cache=args.cache)
