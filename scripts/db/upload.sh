#!/usr/bin/env bash

password=$1

echo "push db image to the repo"
docker login -u="chaimozdsd" -p=${password}
docker push chaimozdsd/db