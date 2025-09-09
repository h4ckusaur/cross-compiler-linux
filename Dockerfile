
    FROM ubuntu:22.04
    WORKDIR /workspace
    RUN apt-get update && apt-get install -y build-essential
    COPY . /workspace
    CMD gcc -o output sample.c
    ARG TZ=America/New_York
    ENV TZ=$TZ
    ENV DEBIAN_FRONTEND=noninteractive
    