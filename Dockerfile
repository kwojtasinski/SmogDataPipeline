ARG PACKAGE_VERSION
FROM smog_data_pipeline:${PACKAGE_VERSION}-development as development
USER root
RUN /opt/poetry/bin/poetry build
WORKDIR /app
FROM python:3.10.12-slim as prod
RUN useradd -m app
USER app
COPY --from=development /app/dist /app/dist/
RUN WHEEL_FILE_PATH=`find /app/dist -iname *.whl | head -n 1` && pip install $WHEEL_FILE_PATH
USER root
RUN rm -rf /app/dist
USER app
