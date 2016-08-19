#!/usr/bin/env bash

REPO_ADDRESS=52.42.224.43:5000

echo "Remove old images and containers"
docker images | grep -P '${REPO_ADDRESS}' | awk '{print $3}' | xargs -I {} docker rmi -f {} || true
docker ps -a | grep -P 'dsd$' | awk '{print$1}' | xargs -I {} docker rm -f {} || true

echo "Pull the latest docker container"
docker pull ${REPO_ADDRESS}/chaimozdsd/dsd:latest

echo "Run the latest docker image"
docker run -p 80:80 -p 8000:8000 --name=dsd -d chaimozdsd/dsd:latest
