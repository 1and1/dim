# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /ndcli

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/ndcli" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    ndcli

# Copy dimclient to the container.
COPY ./dimclient ./dimclient

RUN python -m pip install dimclient/
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=./ndcli/requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY ./ndcli .

# Link the ndcli script to /usr/local/bin/ndcli so it can be run from the command line.
RUN ln -s /ndcli/ndcli /usr/local/bin/ndcli &&\
    echo "complete -C /usr/local/bin/ndcli ndcli" >> /home/ndcli/.bashrc

# Switch to the non-privileged user to run the application.
USER ndcli

# Run the application.
CMD ./ndcli
