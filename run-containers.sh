#!/usr/bin/env bash

docker rm -f codepot-postgres
docker run \
    --name codepot-postgres \
    -d \
    --volumes-from codepot-postgres-data \
    postgres:9.4.1

docker rm -f codepot-redis
docker run \
    --name codepot-redis \
    -v `pwd`/redis-data:/data \
    -d \
    redis:3.0.0

docker rm -f codepot-backend-development-celery
docker run \
    -d \
    --link codepot-redis:redis \
    --env-file=environment \
    -v `pwd`:/app \
    -e C_FORCE_ROOT=true \
    --name codepot-backend-development-celery \
    codepot-backend-development \
    celery -A main.celery.app worker -B -E --loglevel=DEBUG

docker rm -f codepot-backend-development
docker run \
    -d \
    --link codepot-postgres:postgres \
    --link codepot-redis:redis \
    --env-file=environment \
    -p 8080:8080 \
    -p 2222:22 \
    -v `pwd`:/app \
    -v `pwd`/.pycharm_helpers/:/root/.pycharm_helpers \
    --name codepot-backend-development \
    codepot-backend-development

