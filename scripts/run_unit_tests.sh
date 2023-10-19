#!/bin/bash
set -e
echo "Running pytest"
poetry run pytest --record-mode=once
