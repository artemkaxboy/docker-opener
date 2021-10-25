# Docker opener

Manage your docker containers easily

## What is it

It is a tool to simplify everyday work with running containers and compose-projects.

The main features of `docker opener`:

* [Simple shell access to **any** container](#simple-shell-access-to-any-container)
* [Managing containers **without remembering** their full **names**](#managing-containers-without-remembering-their-full-names)
* [**Upgrading images** of running containers](#upgrading-images-of-running-containers)
* [Managing compose-project **without entering** their work **directories**](#managing-compose-project-without-entering-their-work-directories)
* [**Recreating running container**, especially to start on local built images](#recreating-running-container)

## Installation

The `opener` is just a regular docker image it may be used **without installation**: 

```shell
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener [COMMAND] [PARAMS]
```

Linux aliases can be used to **make the command shorter**. For only current terminal session:

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
| `compose-down` | `docker-compose down` |  `opener cdown app` | Stop and remove resources |
| `compose-kill` | `docker-compose kill` |  `opener ckill app` | Stop and remove composes resources |
| `compose-list` | | `opener clist` | Show all compose projects |
| `compose-logs` | `docker-compose logs` |  `opener clogs app` | View output from containers |
| `compose-ps` | `docker-compose ps` |  `opener cps app` | List containers |
| `compose-start` | `docker-compose start` |  `opener cstart app` | Start services |
| `compose-stop` | `docker-compose stop` |  `opener cstop app` | Stop services |
| `compose-top` | `docker-compose top` |  `opener ctop app` | Display the running processes |

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

#### Managing containers without remembering their full names

Any [supported container command](#container-commands-supported-by-opener) can be performed using a short unique container's attribute.

With Example:

```shell
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS        PORTS           NAMES
c072485d836e   postgres  "docker-entrypoint.s…"   6 seconds ago   Up 1 second   5432->5432/tcp  site_database_1
d443a12c54e1   app:v1.0  "/myapp"                 5 seconds ago   Up 3 second   80->8080/tcp    site_app_1
```

The following commands can be performed:

```shell
# restart container by name
opener restart app

# kill container by exposed port
opener kill 5432

# stop container by image name
opener stop postgre
```

#### Upgrading images of running containers

Finding run command of container which was run weeks ago might be a challenge. `opener` can upgrade your containers without manually typing all command.

Example, once run container:

```shell
docker run -d --name=netdata \
  -p 19999:19999 \
  -v netdataconfig:/etc/netdata \
  -v netdatalib:/var/lib/netdata \
  -v netdatacache:/var/cache/netdata \
  -v /etc/passwd:/host/etc/passwd:ro \
  -v /etc/group:/host/etc/group:ro \
  -v /proc:/host/proc:ro \
  -v /sys:/host/sys:ro \
  -v /etc/os-release:/host/etc/os-release:ro \
  --restart unless-stopped \
  --cap-add SYS_PTRACE \
  --security-opt apparmor=unconfined \
  netdata/netdata
```

There is no need to find the whole command again, `opener upgrade` do the job:

```shell
$ opener upgrade netdata
Found container with name `netdata`
CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS                 PORTS                                           NAMES
3348bc4acdb7        netdata/netdata     "/usr/sbin/run.sh"   8 weeks ago         Up 5 weeks (healthy)   0.0.0.0:19999->19999/tcp, :::19999->19999/tcp   netdata

Pulling image `netdata/netdata`...
Recreating `netdata` ...
Copying container `netdata` to `musing_haibt`
Stopping `netdata`
Deleting `netdata`
Renaming container `musing_haibt` to `netdata`
Starting `netdata`
Started `netdata`
```

#### Managing compose-project without entering their work directories

Example, sometime earlier compose-project was started:

```shell
$ docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED       STATUS      PORTS           NAMES
c072485d836e   postgres     "docker-entrypoint.s…"   6 weeks ago   Up 6 week   5432->5432/tcp  site_database_1
d443a12c54e1   app:v1.0     "/myapp"                 6 weeks ago   Up 6 week   80->8080/tcp    site_app_1
...            mongo        ...                      6 weeks ago   Up 6 week   ...             site_mongo_1
...            web:v1.0     ...                      6 weeks ago   Up 6 week   ...             site_web_1
...            worker:v1.0  ...                      6 weeks ago   Up 6 week   ...             site_worker_1
...            worker:v1.0  ...                      6 weeks ago   Up 6 week   ...             site_worker_2
```

It might be a challenge to find compose-file on the server to stop the compose-project, the file could even have been deleted since compose-project was started, in that case the last remaining option was to stop or stop/kill all containers one by one.

`opener compose-stop site` and `opener compose-kill site` will help:

```shell
$ opener compose-kill site
Found compose with name `site`
CONTAINER ID   IMAGE     COMMAND                 CREATED       STATUS     PORTS     NAMES
c072485d836e   postgres  "docker-entrypoint.s…"  6 weeks ago   Up 6 week  5432/tcp  site_database_1
d443a12c54e1   app:v1.0  "/myapp"                6 weeks ago   Up 6 week  80/tcp    site_app_1
...

Killing site_database_1  ... done
Killing site_app_1       ... done
Killing site_mongo_1     ... done
...
```

#### Recreating running container

Example, your project is running with database and many other modules:

```shell
$ docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED       STATUS      PORTS           NAMES
c072485d836e   postgres     "docker-entrypoint.s…"   6 weeks ago   Up 6 week   5432->5432/tcp  site_database_1
d443a12c54e1   app:v1.0     "/myapp"                 6 hours ago   Up 6 hour   80->8080/tcp    site_app_1
...            mongo        ...                      6 weeks ago   Up 6 week   ...             site_mongo_1
...            web:v1.0     ...                      6 weeks ago   Up 6 week   ...             site_web_1
```

You made a new build of one of your modules `app:v1.0` and want to test or run it without restarting the whole compose-project. 

`opener recreate` do it, new container will be created with new build of `app:v1.0`:

```shell
$ docker build -t app:v1.0 .
...
$ opener recreate app
Found container with name `site_app_1` containing `app`
CONTAINER ID  IMAGE     COMMAND   CREATED       STATUS      PORTS         NAMES
d443a12c54e1  app:v1.0  "/myapp"  6 hours ago   Up 6 hour   80->8080/tcp  site_app_1

Recreating `site_app_1` ...
Copying container `site_app_1` to `suspicious_bhabha`
Stopping `site_app_1`
Deleting `site_app_1`
Renaming container `suspicious_bhabha` to `site_app_1`
Starting `site_app_1`
Started `site_app_1`
```

## License

Apache License 2.0, see [LICENSE](https://github.com/artemkaxboy/docker-opener/blob/main/LICENSE).
