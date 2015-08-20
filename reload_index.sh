#!/usr/bin/env bash
django_production_container=`docker ps | grep django_ | grep production | sed 's/ \{2,\}/,/g' | cut -d ',' -f 7 | head -n 1`
docker exec -it $django_production_container python manage.py rebuild_index -v2 --remove --noinput