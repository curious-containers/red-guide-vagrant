#!/usr/bin/env bash

groupadd docker
usermod -aG docker vagrant

apt-get update
apt-get install -y python3-pip python3-venv git docker-engine
