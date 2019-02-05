#!/usr/bin/env bash

set -eu

docker build --pull -t docker.io/copla/grepwrap .
docker run docker.io/copla/grepwrap red-connector-http --version
docker run docker.io/copla/grepwrap grepwrap --help
docker push docker.io/copla/grepwrap
