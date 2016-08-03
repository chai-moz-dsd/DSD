
# Base OS
FROM ubuntu:14.04
MAINTAINER chai-dsd <chai-dsd@thoughtworks.com>

# Install basic tools
RUN apt-get update && apt-get install -y wget curl build-essential libpq-dev git

# Install nginx, postgresql, supervisor
RUN apt-get install -y supervisor postgresql postgresql-contrib nginx

