FROM python:3.10.10-slim-buster as build

ENV TZ=Europe/Moscow
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on
ENV PIP_DEFAULT_TIMEOUT=100

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc curl

WORKDIR /app

RUN pip install poetry

RUN python -m venv .venv

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry export -f requirements.txt | .venv/bin/pip install -r /dev/stdin


FROM python:3.10.10-slim

WORKDIR /app

# Copy installed packages
COPY --from=build /app/.venv .venv
ENV PATH="/app/.venv/bin:$PATH"
ENV DOCKER=True

# Copy application
COPY src .
