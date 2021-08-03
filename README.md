# Docker opener

Shell-in to any docker container easily

## What it is

It is a simple tool to open shell to any running docker container. How to open distroless container? How to open scratch container? It is not a question any more.

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

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener port
Found container with name containing: port
...
```

Connect by port number:

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener 9000
Found container with port containing: 9000
...
```

Connect by container ID:

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener 62f8
Found container with ID containing: 62f8
...
```

### Fetching logs

Fetch logs with `logs|l` command by any known container's property: name, image, port, id. Use any of familiar `docker logs` command options.

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

#### Fetching logs examples

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener kill w
Found container with name `w`
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
bb0f9cecdc4c        nginx               "/docker-entrypoint.…"   About a minute ago   Up About a minute   80/tcp              web

You are killing container `web` [yN]: y
bb0f9cecdc4c050b3abf0cef1cfe098ca5fdc472441f67369ccff3404e3fe1c6
```

### Docker compose commands

Some docker-compose commands are supported by part of name. Available commands:

* `cd|cdown|compose-down` - Stop and remove compose resources
* `cl|clogs|compose-logs` - View output from compose containers
* `ck|ckill|compose-kill` - Kill compose containers
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

The easiest way to use latest version of the utilty is to use latest tag `artemkaxboy/opener:latest` or use it without tag `artemkaxboy/opener`. To update latest version use `update|u` command:

```shell
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener update
Using default tag: latest
latest: Pulling from artemkaxboy/opener
...
```

## Alias

To make the command shorter use linux alias. For current terminal session:

```shell
alias opener='docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener'
```

Or permanently (logout and login or new terminal session required):

```shell
echo "alias opener='docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener'" >> ~/.bash_aliases
```

### Alias usage

After adding alias you can use short form, e.g.:

```shell
# attach to container infrastructure_registry_1
$ opener reg

# view last 200 lines and follow logs of infrastructure compose 
$ opener clogs infra -f --tail 200

# send SIGTERM signal to registry service of infrastructure compose
$ opener ckill infra -s SIGTERM registry
```

## License

Apache License 2.0, see [LICENSE](https://github.com/artemkaxboy/docker-opener/blob/main/LICENSE).
