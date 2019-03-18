FROM docker.io/debian:9.5-slim

RUN apt-get update \
&& apt-get install -y python3-venv \
&& useradd -ms /bin/bash cc

# switch user
USER cc

# install connectors
ENV PATH /home/cc/.local/bin:${PATH}

RUN python3 -m venv /home/cc/.local/red \
&& . /home/cc/.local/red/bin/activate \
&& pip install wheel \
&& pip install red-connector-http==0.3 \
&& mkdir -p /home/cc/.local/bin \
&& ln -s /home/cc/.local/red/bin/red-connector-* /home/cc/.local/bin

# install app
ADD --chown=cc:cc grepwrap /home/cc/.local/bin/grepwrap
