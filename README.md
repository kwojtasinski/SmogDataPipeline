# SmogDataPipeline

## Description
This is a sample ETL pipeline written in Python with polars. My goal here is to show how one can structure the code, turn it into Docker image and run inside Github Actions for easy to setup serverless data processing. Note that this is just a toy projects and in real-life example you should use dedicated compute engines for higher availability and support.

## What is the problem I am trying to solve
I am processing data about the smog levels (PM10, PM25) measured by schools in Poland. This dataset is publicly available and its schema is in English, hence it should be easy to understand. If you would like to learn more visit [ESA](https://esa.nask.pl/) (Polish only) and the [Dataset details page](https://dane.gov.pl/en/dataset/2913,dane-pomiarowe-esa-edukacyjna-siec-antysmogowa/resource/43585/table). This dataset is refreshed on a daily basis, which is reflected in the pipeline execution. Once the JSON data is downloaded, I am doing the simple preprocessing of it and turn it into CSV file.

## How is it done
On top of the Python code I created there is `.github/workflows` directory with Github Actions Workflow definitions. The `ci` is to test the code as part of the Continuous Integration. More interesting is the `run_pipeline.yml` which is responsible for running the code daily (check the cron expression) and published into Github Releases.