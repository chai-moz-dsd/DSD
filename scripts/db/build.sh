#!/usr/bin/env bash

echo "build db image"
docker build -t chaimozdsd/db:9.5 .