#!/usr/bin/env bash

echo "Remove old docker container"
docker ps -a | grep -P 'dsd$' | awk '{print$1}' | xargs -I {} docker rm -f {} || true

echo "Run new docker container"
docker run -p 80:80 -p 8000:8000 --name=dsd -d chai/dsd:$1

echo "login container"
docker exec -it dsd bash

echo "run unit tests"
source ./go ut
