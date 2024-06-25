# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.9.2
FROM python:${PYTHON_VERSION}-slim

RUN apt update \
    && apt install --no-install-suggests --no-install-recommends -y \
    pkg-config gcc curl wget gnupg lsb-release python3-dev \
    && apt-key del 'A4A9 4068 76FC BD3C 4567  70C8 8C71 8D3B 5072 E1F5' \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C \
    && curl -sLo mysql.deb https://dev.mysql.com/get/mysql-apt-config_0.8.19-1_all.deb \
    && DEBIAN_FRONTEND=noninteractive dpkg -i mysql.deb \
    && rm mysql.deb \
    && apt update \
    && apt -y install libmysqlclient-dev \
    && apt purge -y pkg-config curl wget gnupg lsb-release python3-dev

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
    dimuser

WORKDIR /dim

RUN mkdir /etc/dim && chown dimuser:dimuser /etc/dim

COPY --chown=dimuser:dimuser . .

USER dimuser

CMD gunicorn 'app:application' -w 4 -b :8000
