#!/usr/bin/env bash

set -eu

VERSION=5.3.2

docker pull docker.io/debian:9.5-slim
docker build -t docker.io/copla/grepwrap:${VERSION} .
docker run docker.io/copla/grepwrap:${VERSION} ccagent --version
docker run docker.io/copla/grepwrap:${VERSION} grepwrap --help
docker push docker.io/copla/grepwrap:${VERSION}
