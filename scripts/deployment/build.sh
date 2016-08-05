#!/usr/bin/env bash

# Copy Dockerfile to folder where the project root directory is
cp ./chai/Dockerfile ./

# Build docker image
sudo docker build -t chai/dsd .