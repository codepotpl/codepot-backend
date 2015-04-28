#!/usr/bin/env bash

docker rm -f codepot-postgres
docker run \
    --name codepot-postgres \
    -e POSTGRES_PASSWORD=lolpass \
    -d \
    --volumes-from codepot-postgres-data \
    postgres:9.4.1

docker rm -f codepot-redis
docker run \
    --name codepot-redis \
    -v `pwd`/redis-data:/data \
    -d \
    redis:3.0.0

docker rm -f codepot-backend-development
docker run \
    -d \
    --link codepot-redis:redis \
    --link codepot-postgres:postgres \
    -p 8080:8080 \
    -p 2222:22 \
    -v `pwd`:/app \
    -v `pwd`/.pycharm_helpers/:/root/.pycharm_helpers \
    --name codepot-backend-development \
    codepot-backend-development