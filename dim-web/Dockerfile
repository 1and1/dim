# syntax=docker/dockerfile:1
FROM debian:bullseye AS builder

RUN apt update \
    && apt install -y \
    python2 \
    npm

WORKDIR /dim-web

COPY package.json .
RUN npm install

COPY . .

ARG DIM_LOGIN
ARG DIM_RPC
ARG LOGIN
ARG LOGOUT
ARG BASE_URL

RUN build/replace-process-env-docker-build.sh && cat config/prod.env.js

RUN npm run build

# Run the final image
FROM nginx:1.21 AS final

# Copy the build files to the nginx server
COPY  --from=builder /dim-web /var/www/html
COPY --from=builder /dim-web/dist/index.html /var/www/html/dist/static/
COPY config/dim-web.nginx.conf /etc/nginx/conf.d/
