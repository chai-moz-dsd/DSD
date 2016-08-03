
# Base OS
FROM ubuntu:14.04
MAINTAINER chai-dsd <chai-dsd@thoughtworks.com>

RUN apt-get update

# Install basic tools
RUN apt-get install -y wget curl build-essential libpq-dev git openssl

# Install Python
ARG python_version=3.5.2
RUN cd /opt \
    && wget "https://www.python.org/ftp/python/$python_version/Python-$python_version.tgz" \
    && tar -xzvf Python-$python_version.tgz \
    && ./Python-$python_version/configure \
    && make \
    && make install \
    && ln -fs /opt/Python-$python_version/Python/ /usr/bin/python \
    && ln -s /usr/local/bin/python3.5 /usr/local/bin/python

# Install supervisor nginx, supervisor, pip
RUN apt-get install -y supervisor nginx python-pip

# Install virtualenv
RUN pip install virtualenv
