FROM docker.io/debian:9.3-slim

RUN apt-get update \
&& apt-get install -y python3-pip \
&& useradd -ms /bin/bash cc

# install cc-core
USER cc

RUN pip3 install --no-input --user cc-core==3.1.0

ENV PATH="/home/cc/.local/bin:${PATH}"
ENV PYTHONPATH="/home/cc/.local/lib/python3.5/site-packages/"

# install app
ADD --chown=cc:cc grepwrap /home/cc/.local/bin/grepwrap
