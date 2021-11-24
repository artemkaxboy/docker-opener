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

    @classmethod
    def get_container_by_id(cls, container_id):
        return cls.get_docker().containers.get(container_id)

    # @classmethod
    # def get_current_container_image(cls) -> Image:
    #     hostname = socket.gethostname()
    #     try:
    #         container: Container = cls.get_docker().containers.get(hostname)
    #         docker_container = DockerContainer(container)
    #         return docker_container.get_image_name()
    #     except APIError:
    #         raise ObjectNotFoundError("Current container image not found. Is the app run in docker?")
