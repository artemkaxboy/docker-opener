# Docker opener

Shell-in to any docker container easily

## What it is

It is a simple tool to open shell to any running docker container. How to open distroless container? How to open scratch container? It is not a question anymore.

## Installation

The `opener` is just a regular docker image it may be used without installation, like: 

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

## How to use

### Connecting to container

Connect to any running container by typing any known attribute: name, image, exposed port, id.

#### Connecting examples

Run any container:

```shell
$ docker run -d --name docker-web portainer/portainer-ce
62f87fb2...
```

Connect by name:

```shell
$ opener web
Found container with name containing: web
CONTAINER ID        IMAGE                    COMMAND             CREATED             STATUS              PORTS                NAMES
62f87fb2ce5f        portainer/portainer-ce   "/portainer"        29 seconds ago      Up 28 seconds       8000/tcp, 9000/tcp   docker-web
Installing busybox...
Connecting...
/ # hostname
62f87fb2ce5f
/ # exit
Removing busybox...
```

Connect by image name:

```shell
$ opener port
Found container with name containing: port
...
```

Connect by port number:

```shell
$ opener 9000
Found container with port containing: 9000
...
```

Connect by container ID:

```shell
$ opener 62f8
Found container with ID containing: 62f8
...
```

### Special commands

| Command | Result |
| --- | --- |
| help | Show help message |
| update | Update (pull) `opener` image |
| version | Show `opener` version |

### Container commands supported by opener

| Command | Docker example | Opener short example | Result |
| --- | --- | --- | --- |
| `--` | | `docker -- ng` | Run new shell process in the container and connect |
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

#### Fetching logs examples

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener logs web -f
Found container with name containing: web
CONTAINER ID        IMAGE                    COMMAND             CREATED             STATUS              PORTS                NAMES
62f87fb2ce5f        portainer/portainer-ce   "/portainer"        7 minutes ago       Up 12 seconds       8000/tcp, 9000/tcp   docker-web
Fetching logs for 62f87fb2ce5f978842b65beebffcc87ff09f8a9e3f2f4540da267bd37da4860c
2021/07/27 16:40:34 server: ...
...
```

### Kill container

Kill container with `kill|k` command by any known container's property: name, image, port, id. Use any of familiar `docker kill` command options.

#### Kill examples

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener kill w
Found container with name `w`
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
bb0f9cecdc4c        nginx               "/docker-entrypoint.…"   About a minute ago   Up About a minute   80/tcp              web

You are killing container `web` [yN]: y
bb0f9cecdc4c050b3abf0cef1cfe098ca5fdc472441f67369ccff3404e3fe1c6
```

### Recreate container

Recreate container with `recreate` command by any known container's property: name, image, port, id. The command will kill current container and create the same one.

### Upgrade container

Upgrade container with `upgrade` command by any known container's property: name, image, port, id. The command will pull container's image, kill current container and create identical one using updated image.

### Docker compose commands

Some docker-compose commands are supported by part of name. Available commands:

* `cd|cdown|compose-down` - Stop and remove compose resources
* `cl|clogs|compose-logs` - View output from compose containers
* `ck|ckill|compose-kill` - Kill compose containers
* `cps|compose-ps` - List containers
* `cstart|compose-start` - Start compose services
* `cstop|compose-stop` - Stop compose services
* `ct|ctop|compose-top` - Display the running compose processes

#### Compose commands examples

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener compose-logs infra -f registry
Found compose with name containing `infra`: infrastructure
Fetching logs for compose
Attaching to infrastructure_registry_1
registry_1   | ...
```

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener compose-stop infra
Found compose with name containing `infra`: infrastructure
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                                                                                  NAMES
de42f6ae4b6c        portainer/portainer-ce   "/portainer"             5 hours ago         Up 5 hours          0.0.0.0:8000->8000/tcp, :::8000->8000/tcp, 0.0.0.0:9000->9000/tcp, :::9000->9000/tcp   infrastructure_portainer_1
8fd435e39c11        registry:2               "/entrypoint.sh /etc…"   2 weeks ago         Up 45 hours         0.0.0.0:5000->5000/tcp, :::5000->5000/tcp                                              infrastructure_registry_1

Stopping infrastructure_portainer_1 ... done
Stopping infrastructure_registry_1  ... done
```

### Update

The easiest way to use the latest version of the utility is to use the latest tag `artemkaxboy/opener:latest` or use it without tag `artemkaxboy/opener`. To update the latest version use `update|u` command:

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener update
Using default tag: latest
latest: Pulling from artemkaxboy/opener
...
```

## License

Apache License 2.0, see [LICENSE](https://github.com/artemkaxboy/docker-opener/blob/main/LICENSE).
