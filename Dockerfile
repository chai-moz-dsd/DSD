FROM ubuntu:14.04
MAINTAINER chai-dsd <chai-dsd@thoughtworks.com>

# Install basic tools, supervisor and pip
RUN apt-get update \
    && apt-get install -y wget curl build-essential libpq-dev git openssl

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

# install supervisor and pip
RUN apt-get install -y supervisor python-pip

# Install nginx uwsgi and config nginx uwsgi supervisor
# !!! Use pip3 to install uwsgi, otherwise uwsgi will use python2
RUN apt-get install -y python-dev nginx \
    && pip3 install uwsgi
COPY ./chai/scripts/ /opt/app/chai/scripts/

RUN mkdir -p /etc/uwsgi/sites \
    && rm /etc/nginx/sites-enabled/default \
    && ln -sf /opt/app/chai/scripts/config/dsd.uwsgi.ini /etc/uwsgi/sites/dsd.uwsgi.ini \
    && ln -sf /opt/app/chai/scripts/config/dsd.nginx.config /etc/nginx/sites-enabled \
    && ln -sf /opt/app/chai/scripts/config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf


##############################################################################
## install NodeJS
##############################################################################
# verify gpg and sha256: http://nodejs.org/dist/v0.10.30/SHASUMS256.txt.asc
RUN gpg --keyserver pool.sks-keyservers.net --recv-keys 7937DFD2AB06298B2293C3187D33FF9D0246406D 114F43EE0176B71C7BC219DD50A3051F888C628D \
    && curl -SLO "http://nodejs.org/dist/v0.10.21/node-v0.10.21-linux-x64.tar.gz" \
    && curl -SLO "http://nodejs.org/dist/v0.10.21/SHASUMS256.txt.asc" \
    && gpg --verify SHASUMS256.txt.asc \
    && grep " node-v0.10.21-linux-x64.tar.gz\$" SHASUMS256.txt.asc | sha256sum -c - \
    && tar -xzf "node-v0.10.21-linux-x64.tar.gz" -C /usr/local --strip-components=1 \
    && curl -SLO "http://nodejs.org/dist/v0.10.21/SHASUMS256.txt.asc" \
    && rm "node-v0.10.21-linux-x64.tar.gz" SHASUMS256.txt.asc \
    && npm install -g npm@1.4.28 \
    && npm install -g npm@"1.3.11" \
    && npm cache clear

# Install virtualenv
RUN pip install virtualenv

# Create dsd virtual env
RUN virtualenv ~/.virtualenvs/dsd && virtualenv -p /usr/local/bin/python ~/.virtualenvs/dsd

##############################################################################
## Install dependenices
##############################################################################
COPY ./chai/requirements.txt /opt/app/chai/requirements.txt
RUN virtualenv ~/.virtualenvs/dsd
RUN /bin/bash -c "source ~/.virtualenvs/dsd/bin/activate && cd /opt/app/chai && pip install -r requirements.txt"

COPY ./chai/dsd/client/package.json /opt/app/chai/dsd/client/package.json
COPY ./chai/dsd/client/bower.json /opt/app/chai/dsd/client/bower.json
RUN cd /opt/app/chai/dsd/client && npm install
RUN cd /opt/app/chai/dsd/client && npm install -g bower
RUN cd /opt/app/chai/dsd/client && bower install --allow-root

# Set work dir
WORKDIR /opt/app/chai

# Install dependenices
RUN /bin/bash -c "source ~/.virtualenvs/dsd/bin/activate && pip install -r requirements.txt"

# Copy source code
COPY ./chai /opt/app/chai

# Collect static files
RUN /bin/bash -c "source ~/.virtualenvs/dsd/bin/activate && python manage.py collectstatic --no-input"

# Expose ports
EXPOSE 80

# Entrypoint
CMD ["/usr/bin/supervisord"]

