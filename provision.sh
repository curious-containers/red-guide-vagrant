#!/usr/bin/env bash

groupadd docker
usermod -aG docker vagrant

apt-get update
apt-get install -y apt-utils git python3-pip

curl -fsSL test.docker.com | sh

su vagrant -c "mkdir -p ~/.local/bin"
