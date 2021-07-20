# Docker opener

Shell-in to any docker container easily

## What it is

It is a simple tool to open shell to any running docker container. How to open distroless container? How to open scratch container? It is not a question any more.

## How to use

Run command:

```bash
docker run -it -v /var/run/docker.sock:/var/run/docker.sock artemkaxboy/opener <target>
```

`<target>` - is a name (or a part of it) of container you want to connect to. It is looking for first match of name or part, when you have a few containers with similar name it shell-in first found.

## License

Apache License 2.0, see [LICENSE](https://github.com/artemkaxboy/docker-opener/blob/main/LICENSE).
