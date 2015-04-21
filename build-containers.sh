#!/usr/bin/env bash

docker build --no-cache --tag codepot-backend .
docker build --no-cache --tag codepot-backend-development --file Dockerfile-development .
