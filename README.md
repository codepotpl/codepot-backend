#Development

1. Start `boot2docker`.
2. Run `./build-containers.sh`.
3. Run `./run-containers.sh`.
4. Add PyCharm python interpreter: 
  * host: `192.168.59.103`
  * port: `2222`
  * username: `root`
  * password: `codepot`
  * python interpreter path: `/usr/local/bin/python`
5. Add run configuration:
  * host: `0.0.0.0`
  * port: `8080`
  * working directory: `/app`
  * path mappings `<your absolute path to project root>=/app`

KNOWN ISSUES:
* postgres isn't persistent ;/