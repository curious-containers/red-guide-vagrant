#!/usr/bin/env bash

groupadd docker
usermod -aG docker vagrant

sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
dnf install -y nano git redhat-rpm-config gcc python3-devel docker-ce

systemctl enable docker
systemctl start docker
