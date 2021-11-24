import docker as docker
from docker import DockerClient
from docker.errors import DockerException


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
