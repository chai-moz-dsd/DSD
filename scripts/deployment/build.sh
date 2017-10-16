#!/usr/bin/env bash

# Copy Dockerfile to folder where the project root directory is
echo "Copy Dockerfile"
cp ./${3}/Dockerfile ./

echo "Build docker image"
docker build -t chaimozdsd/dsd:${1} .

password=${2}

echo "push docker image to the repo"
docker login -u="sakura164995249" -p=${password}
docker push chaimozdsd/dsd:${1}
