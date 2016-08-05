#!/usr/bin/env bash

docker rm dsd

docker run -p 80:80 -p 8000:8000 --name=dsd -d chai/dsd