#!/usr/bin/env bash

docker rm -f -v codepot-postgres-data
docker create --name codepot-postgres-data -v /var/lib/postgresql postgres:9.4.1