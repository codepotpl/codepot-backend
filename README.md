# Development

1. Start `boot2docker`.
2. Run `./build-containers.sh`.
3. Run `./recreate-database.sh`. **Important**: running this script will remove previous postgres data.
4. Run `./run-containers.sh`.
5. Add PyCharm python interpreter: 
  * host: `192.168.59.103`
  * port: `2222`
  * username: `root`
  * password: `codepot`
  * python interpreter path: `/usr/local/bin/python`
6. Add run configuration:
  * host: `0.0.0.0`
  * port: `8080`
  * working directory: `/app`
  * path mappings `<your absolute path to project root>=/app`

KNOWN ISSUES:
* Postgres data is persistent only in boot2docker VM. Moving it to OsX host would be awesome but it requires some fixes
  with permissions... :( More info [here](https://github.com/boot2docker/boot2docker/issues/581).
  
# Staging/Production

1. Run `docker-compose build`.
2. Run `docker-compose up -d`.

## To migrate database:

1. Run `docker ps` and find instance name you are looking for.
2. Run `docker exec -it <instance name> python manage.py migrate`
