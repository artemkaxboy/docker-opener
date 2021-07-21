# Docker opener

Shell-in to any docker container easily

## What it is

It is a simple tool to open shell to any running docker container. How to open distroless container? How to open scratch container? It is not a question any more.

## How to use

Run command:

```bash
docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener <target>
```

`<target>` - container attribute to connect to. Following attributes supported: exact name, part of name, part of image name, part of ID, part of opened port.

## Example

Run any container:

```bash
$ docker run -d --name distroless example/distroless
5c4e8a062e48...
```

Connect by name:

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener distroless
Found container with name: distroless
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS          PORTS     NAMES
5c4e8a062e48   example/distroless   "/docker-entrypoint.…"   58 seconds ago   Up 57 seconds   80/tcp    distroless
/ # hostname
5c4e8a062e48
/ # exit
```

Connect by image name:

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener examp
Found container with image containing: examp
CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS         PORTS     NAMES
5c4e8a062e48   example/distroless   "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   80/tcp    distroless
/ # hostname
5c4e8a062e48
/ # exit
```

Connect by port number:

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener 80
Found container with port containing: 80
...
```

Connect by container ID:

```bash
$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener 5c4e
Found container with ID containing: 5c4e
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
