ARG PYTHON_BASE_VERSION=3.10.12
FROM python:${PYTHON_BASE_VERSION}-slim
ARG POETRY_VERSION=1.6.1
RUN groupadd --gid 1000 dev && useradd --uid 1000 --gid 1000 -m dev
USER dev
WORKDIR /app
ENV PATH=$PATH:/home/dev/poetry/bin
RUN python -m venv /home/dev/poetry && \
    /home/dev/poetry/bin/pip install poetry==${POETRY_VERSION}
COPY --chown=dev:dev pyproject.toml poetry.lock ./
# workaround, so poetry dependencies can be cached
RUN mkdir smog_data_pipeline && touch README.md && touch smog_data_pipeline/__init__.py
RUN poetry --version && poetry install
COPY --chown=dev:dev . .
RUN poetry install
CMD [ "/bin/bash" ]
