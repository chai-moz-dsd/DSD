#!/usr/bin/env bash

echo "push docker image to the repo"
docker login -u="chaimozdsd" -p=$1
docker push chaimozdsd/dsd