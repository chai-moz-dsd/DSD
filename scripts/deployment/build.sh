#!/usr/bin/env bash

# Copy Dockerfile to folder where the project root directory is
echo "Copy Dockerfile"
cp ./${3}/Dockerfile ./

echo "Build docker image"
docker build -t chaimozdsd/dsd:${1} .

echo "Remove old images"
docker images | grep -P '^\S+dsd\s+([0-9]+)\b' | \
awk 'BEGIN {BASELINE="'${1}'"}{if($2 < BASELINE) print $1":"$2}' | xargs -I {} docker rmi -f {} || true

docker images | grep "^<none>" | awk 'NR >= 1 {print $3}' | xargs -I {} docker rmi -f {} || true

password=${2}

echo "push docker image to the repo"
docker login -u="chaimozdsd" -p=${password}
docker push chaimozdsd/dsd:${1}
