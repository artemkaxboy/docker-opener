# Docker opener

Shell-in to any docker container easily

## What it is

It is a simple tool to open shell to any running docker container. How to open distroless container? How to open scratch container? It is not a question any more.

## How to use

### Connecting to container

Connect to any running container by typing any known attribute: name, image, exposed port, id.

#### Connecting examples

Run any container:

```bash
$ docker run -d --name docker-web portainer/portainer-ce
62f87fb2...
```

Connect by name:

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener web
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

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener port
Found container with name containing: port
...
```

Connect by port number:

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener 9000
Found container with port containing: 9000
...
```

Connect by container ID:

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener 62f8
Found container with ID containing: 62f8
...
```

### Fetching logs

Fetch logs with `logs|l` command by any known container's property: name, image, port, id. Use any of familiar `docker logs` command options.

#### Fetching logs examples

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener logs web -f
Found container with name containing: web
CONTAINER ID        IMAGE                    COMMAND             CREATED             STATUS              PORTS                NAMES
62f87fb2ce5f        portainer/portainer-ce   "/portainer"        7 minutes ago       Up 12 seconds       8000/tcp, 9000/tcp   docker-web
Fetching logs for 62f87fb2ce5f978842b65beebffcc87ff09f8a9e3f2f4540da267bd37da4860c
2021/07/27 16:40:34 server: ...
...
```

### Fetching compose logs

Fetch compose logs by compose's project name. Use any of familiar `docker-compose logs` command options.

### Fetching compose logs examples

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener compose-logs infra -f registry
Found compose with name containing `infra`: infrastructure
Fetching logs for compose
Attaching to infrastructure_registry_1
registry_1   | ...
```

### Update

The easiest way to use latest version of the utilty is to use latest tag `artemkaxboy/opener:latest` or use it without tag `artemkaxboy/opener`. To update latest version use `update|u` command:

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener update
Using default tag: latest
latest: Pulling from artemkaxboy/opener
...
```

## Alias

To make the command shorter use linux alias. For current terminal session:

```bash
alias opener='docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener'
```

Or permanently:

```bash
echo "alias opener='docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener'" >> ~/.bash_aliases
```

## License

Apache License 2.0, see [LICENSE](https://github.com/artemkaxboy/docker-opener/blob/main/LICENSE).
