#!/usr/bin/env bash

tag=$1

echo "Run new docker container build = ${tag}"
docker run -p 80:80 -p 8000:8000 --name=dsd-${tag} -d chaimozdsd/dsd:${tag}

echo "login container and run unit tests"
OUT=$(docker exec dsd-${tag} bash ./go ut)
echo ${OUT}
if [ ${OUT} -ne 0 ]; then
    echo "Remove current container while the test is down."
    docker rm -f dsd-${tag} || true
fi

echo "Remove current container"
docker ps -a | grep -P dsd-${tag} | awk '{print$1}' | xargs -I {} docker rm -f {} || true
