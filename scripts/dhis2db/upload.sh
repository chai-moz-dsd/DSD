#!/usr/bin/env bash

password=$1

echo "push dhis2_db image to the repo"
docker login -u="chaimozdsd" -p=${password}
docker push chaimozdsd/dhis2_db