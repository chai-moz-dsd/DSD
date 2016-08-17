#!/usr/bin/env bash

# Copy Dockerfile to folder where the project root directory is
echo "Copy Dockerfile"
cp ./${JOB_NAME}/Dockerfile ./

echo "Build docker image"
docker build -t chai/dsd:${BUILD_NUMBER} .

echo "Remove old images"
docker images | grep -P '^\S+dsd\s+([0-9]+)\b' | awk 'BEGIN {BASELINE=${BUILD_NUMBER}}{if($2 < BASELINE) print $1":"$2}' | xargs -I {} docker rmi -f {} || true
