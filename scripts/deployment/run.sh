#!/usr/bin/env bash

echo "Remove old docker container"
docker rm -f dsd

echo "Run new docker container"
docker run -p 80:80 -p 8000:8000 --name=dsd -d chai/dsd:${BUILD_NUMBER}