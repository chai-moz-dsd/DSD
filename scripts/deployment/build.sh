#!/usr/bin/env bash

# Copy Dockerfile to folder where the project root directory is
echo "Copy Dockerfile"
cp ./${JOB_NAME}/Dockerfile ./

echo "Build docker image"
sudo docker build -t chai/dsd:${BUILD_NUMBER} .