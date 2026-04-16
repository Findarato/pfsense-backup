FROM python:3.14-trixie
# Thanks to the following resources for helping me build this Dockerfile:
# https://github.com/instrumentisto/geckodriver-docker-image/blob/main/Dockerfile

LABEL org.opencontainers.image.authors="findarato@gmail.com"
LABEL org.opencontainers.image.description="pfSense backup script"
LABEL org.opencontainers.image.version="1.0"

ARG firefox_ver=149.0.2
ARG geckodriver_ver=0.36.0
ARG build_rev=0


RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends --no-install-suggests \
            ca-certificates \
 && update-ca-certificates

WORKDIR /app 

RUN mkdir -p /app/backups

COPY src/ .env requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV MOZ_HEADLESS=1


ENTRYPOINT ["python", "main.py"]