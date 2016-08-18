#!/usr/bin/env bash

echo "untag old image"
docker images | grep -P '127.0.0.1:5000' | awk '{print $1}' | xargs -I {} docker rmi {} || true

echo "push docker image to the repo"
docker images | grep -P '^\S+dsd\s+([0-9]+)\b' | awk '{print $3}' | \
xargs -I {} docker tag {} 127.0.0.1:5000/chai/dsd || true

docker push 127.0.0.1:5000/chai/dsd