#!/usr/bin/env bash

tag=$1

echo "Run new docker container"
docker run -p 80:80 -p 8000:8000 --name=dsd-${tag} -d chaimozdsd/dsd:${tag}
if [ $? -ne 0 ]; then
    docker ps -a | grep -P 'dsd-${tag}$' | awk '{print$1}' | xargs -I {} docker rm -f {} || true
fi

echo "login container and run function tests"
docker exec dsd-${tag} bash ./go ft
if [ $? -ne 0 ]; then
    docker ps -a | grep -P 'dsd-${tag}$' | awk '{print$1}' | xargs -I {} docker rm -f {} || true
fi

echo "Remove old docker container"
docker ps -a | grep -P 'dsd-${tag}$' | awk '{print$1}' | xargs -I {} docker rm -f {} || true
