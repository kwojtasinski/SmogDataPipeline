#!/bin/bash
set -e
if command -v poetry &> /dev/null
then
    POETRY=poetry
else
    POETRY="/opt/poetry/bin/poetry"
fi
echo "Running black format"
$POETRY run black .
echo "Running ruff fix"
$POETRY run ruff --fix .
