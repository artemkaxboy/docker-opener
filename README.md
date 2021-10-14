# Docker opener

Manage your docker containers easily

## What it is

It is a tool to simplify everyday work with running containers and compose-projects.

The main features of docker opener:

* Simple shell access to any container
* Managing containers without remembering their full names
* Upgrading images of running containers
* Managing compose-project without entering their work directories
* Recreating running container, especially to start on local built images

## Installation

The `opener` is just a regular docker image it may be used without installation: 

```shell
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener [COMMAND] [PARAMS]
```

Linux aliases can be used to make the command shorter. For only current terminal session:

```shell
alias opener='docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener'
```

Or permanently (re-login required):

```shell
echo "alias opener='docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener'" >> ~/.bash_aliases
```

### Alias usage

After adding alias you can use short form:

```shell
# long
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener [COMMAND] [PARAMS]
# short
opener [COMMAND] [PARAMS]
```

### Update

```shell
$ opener update
Using default tag: latest
latest: Pulling from artemkaxboy/opener
...
```

## How to use

### Commands

#### Special commands

| Command | Result |
| --- | --- |
| `help` | Show help message |
| `update` | Update (pull) `opener` image |
| `version` | Show `opener` version |

#### Container commands supported by opener

| Command | Regular docker example | Opener short example | Result |
| --- | --- | --- | --- |
| `--` | `docker exec -it nginx bash` | `docker -- ng` | Run new shell process in the container and connect |
| `attach` | `docker attach nginx` | `opener a ng` | Attach local standard input, output, and error streams to a running container |
| `exec` | `docker exec nginx date` | `opener e ng date` | Run a command in a running container |
| `inspect` | `docker inspect nginx` | `opener i ng` | Return low-level information on Docker objects |
| `kill` | `docker kill nginx` | `opener k ng` | Kill one or more running containers |
| `logs` | `docker logs nginx -f` | `opener l ng -f` | Fetch the logs of a container |
| `pause` | `docker pause nginx` | `opener p ng` | Pause all processes within one or more containers |
| `recreate` | | `opener recreate ng` | Kill and Remove running container and Create and Run the same container |
| `restart` | `docker restart nginx` | `opener res ng` | Restart one or more containers |
| `rm` | `docker rm nginx` | `opener rm ng` | Remove one or more containers |
| `start` | `docker start nginx` | `opener sta ng` | Start one or more stopped containers |
| `stop` | `docker stop nginx` | `opener sto ng` | Stop one or more running containers |
| `unpause` | `docker unpause nginx` | `opener unpause ng` | Unpause all processes within one or more containers |
| `upgrade` | | `opener upgrade ng` | Pull container's image, Kill and Remove running container, Create and Run the same container with updated image |

`ng` - an example of how to use a part of a name of needed container, e.g. `nginx` -> `ng`

#### Compose commands supported by opener

All regular docker-compose examples must be run in the compose.yaml file directory, whereas opener compose command only requires a part of the name of a running compose-project.

| Command | Regular docker-compose example | Opener short example | Result |
| --- | --- | --- | --- |
| `down` | `docker-compose down` |  `opener cdown app` | Stop and remove resources |
| `logs` | `docker-compose logs` |  `opener clogs app` | View output from containers |
| `kill` | `docker-compose kill` |  `opener ckill app` | Stop and remove composes resources |
| `ps` | `docker-compose ps` |  `opener cps app` | List containers |
| `start` | `docker-compose start` |  `opener cstart app` | Start services |
| `stop` | `docker-compose stop` |  `opener cstop app` | Stop services |
| `top` | `docker-compose top` |  `opener ctop app` | Display the running processes |

`app` - is a name/part of a name of running compose-project, which is usually equals to the name of docker-compose file's directory.

All "Regular docker-compose examples" must be run in the directory of the compose-file, whereas opener commands can be run from anywhere.

### Examples

#### Simple shell access to any container

To access container shell `opener` checks if the container already have one `bash` or `sh` and use it, if not `opener` will install busybox into the running target container and connect to the container using it. Busybox will be wiped out from the container on disconnecting.

Run any container:

```shell
$ docker run -d --name docker-web portainer/portainer-ce
62f87fb2...
```

Connect it by `name`:

```shell
$ opener web
Found container with name containing: web
...
Installing busybox...
Connecting...
/ # hostname
62f87fb2ce5f
/ # exit
Removing busybox...
```

By `image name`:

```shell
$ opener port
Found container with image `portainer/portainer-ce` containing `port`
...
```

By `exposed port number`:

```shell
$ opener 9000
Found container with port containing: 9000
...
```

By `ID`:

```shell
$ opener 62f8
Found container with ID containing: 62f8
...
```

## License

Apache License 2.0, see [LICENSE](https://github.com/artemkaxboy/docker-opener/blob/main/LICENSE).
