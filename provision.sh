#!/usr/bin/env bash

dnf install -y docker-engine git
groupadd docker
usermod -aG docker vagrant
systemctl enable docker
systemctl start docker
