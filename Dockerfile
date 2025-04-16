FROM python:3.12-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.2 \
    POETRY_HOME=/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

RUN apt update && \
    apt install curl -y && \
    curl -sSL https://install.python-poetry.org | python -

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

COPY . .
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

EXPOSE 8000
ENTRYPOINT [ "bash", "entrypoint.sh" ]
