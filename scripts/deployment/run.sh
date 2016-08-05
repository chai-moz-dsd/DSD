#!/usr/bin/env bash

echo "Remove old docker container"
sudo docker rm -f dsd

echo "Run new docker container"
sudo docker run -p 80:80 -p 8000:8000 --name=dsd -d chai/dsd