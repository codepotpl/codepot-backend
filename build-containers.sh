#!/usr/bin/env bash

docker build --tag codepot-backend .
docker build --tag codepot-backend-development --file Dockerfile-development .
