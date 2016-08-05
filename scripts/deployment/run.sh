#!/usr/bin/env bash

# Remove old docker container
sudo docker rm -f dsd

# Run new docker container
sudo docker run -p 80:80 -p 8000:8000 --name=dsd -d chai/dsd