import socket

import docker as docker
from docker import DockerClient
from docker.errors import DockerException, APIError
from docker.models.containers import Container
from docker.models.images import Image

from errors import ObjectNotFoundError


class DockerEngine:
    docker_client: DockerClient = None

    @classmethod
    def is_client_available(cls):
        try:
            cls.docker_client = docker.client.from_env()
            return True
        except DockerException:
            return False

    @classmethod
    def get_docker(cls):
        if cls.docker_client is None:
            cls.docker_client = docker.client.from_env()

        return cls.docker_client

    @classmethod
    def get_current_container_image(cls) -> Image:
        hostname = socket.gethostname()
        try:
            print(hostname)
            container: Container = cls.get_docker().containers.get(hostname)
            return container.image
        except APIError:
            raise ObjectNotFoundError("Current container image not found. Is the app run in docker?")
