FROM ubuntu:14.04
MAINTAINER chai-dsd <chai-dsd@thoughtworks.com>

# Install basic tools, supervisor and pip
RUN apt-get update \
    && apt-get install -y wget curl build-essential libpq-dev git openssl libsqlite3-dev postgresql-contrib

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

# Install virtualenv
RUN pip install virtualenv

# Create dsd virtual env
RUN virtualenv -p /usr/local/bin/python ~/.virtualenvs/dsd

# Copy requirements
COPY ./chai/requirements.txt /opt/app/chai/requirements.txt

# Set work dir
WORKDIR /opt/app/chai

# Install dependenices
RUN /bin/bash -c "source ~/.virtualenvs/dsd/bin/activate && pip install -r requirements.txt"

# Copy source code
COPY ./chai /opt/app/chai

RUN mkdir -p /etc/uwsgi/sites \
    && rm /etc/nginx/sites-enabled/default \
    && ln -sf /opt/app/chai/scripts/config/dsd.uwsgi.ini /etc/uwsgi/sites/dsd.uwsgi.ini \
    && ln -sf /opt/app/chai/scripts/config/dsd.nginx.config /etc/nginx/sites-enabled \
    && ln -sf /opt/app/chai/scripts/config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Collect static files
RUN /bin/bash -c "source ~/.virtualenvs/dsd/bin/activate && python manage.py collectstatic --no-input"

# Expose ports
EXPOSE 80 443

# Entrypoint
CMD ["/usr/bin/supervisord"]

