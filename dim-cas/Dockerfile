# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.9.2
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

WORKDIR /cas

RUN mkdir /etc/cas && chown appuser:appuser /etc/cas

COPY --chown=appuser:appuser . .

USER appuser

CMD gunicorn 'login:app' -w 4 -b :8000
