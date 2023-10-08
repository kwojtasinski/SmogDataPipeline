#!/bin/bash
VERSION=${1:-`poetry version -s`}
poetry version $VERSION
poetry build

if command -v docker &> /dev/null
then
    docker build . -t smog_data_pipeline:$VERSION-development -f dev.Dockerfile
    docker build . --build-arg PACKAGE_VERSION=$VERSION -t smog_data_pipeline:$VERSION-latest
fi
