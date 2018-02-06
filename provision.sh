#!/usr/bin/env bash

dnf install -y nano git docker-engine redhat-rpm-config gcc python3-devel
groupadd docker
usermod -aG docker vagrant
systemctl enable docker
systemctl start docker
