ARG PYTHON_BASE_VERSION=3.10.12
FROM python:${PYTHON_BASE_VERSION}-slim
ARG POETRY_VERSION=1.6.1
WORKDIR /app
RUN python -m venv /opt/poetry && \
    /opt/poetry/bin/pip install poetry==${POETRY_VERSION} && \
    echo 'PATH=$PATH:/opt/poetry/bin/' >>  ~/.bashrc && useradd -m dev && \
    echo 'export PATH=$PATH:/opt/poetry/bin' >> /home/dev/.bashrc && \
    echo 'export PATH=$PATH:/opt/poetry/bin' >> /home/dev/.profile && \
    chown dev:dev /app
USER dev
COPY pyproject.toml poetry.lock ./
# workaround, so poetry dependencies can be cached
RUN mkdir smog_data_pipeline && touch README.md && touch smog_data_pipeline/__init__.py
RUN /opt/poetry/bin/poetry --version  && /opt/poetry/bin/poetry install
COPY . .
RUN /opt/poetry/bin/poetry install
ENTRYPOINT [ "/bin/bash" ]
