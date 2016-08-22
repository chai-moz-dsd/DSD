#!/usr/bin/env bash

tag=${BUILD_NUMBER}

# Copy Dockerfile to folder where the project root directory is
echo "Copy Dockerfile"
cp ./${JOB_NAME}/Dockerfile ./

echo "Build docker image"
docker build -t chaimozdsd/dsd:${tag} .

echo "Remove old images"
docker images | grep -P '^\S+dsd\s+([0-9]+)\b' | \
awk 'BEGIN {BASELINE="'${tag}'"}{if($2 < BASELINE) print $1":"$2}' | xargs -I {} docker rmi -f {} || true

echo "tag latest image"
docker rmi chaimozdsd/dsd:latest
docker tag chaimozdsd/dsd:${tag} chaimozdsd/dsd:latest

docker images | grep "^<none>" | awk 'NR >= 1 {print $3}' | xargs -I {} docker rmi -f {} || true
