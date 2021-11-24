import socket

from docker.models.containers import Container

from dockerbuild.docker_opener.docker_engine.docker_engine import DockerEngine
from errors import ObjectNotFoundError


class DockerContainer(Container):

    def __init__(self, container):
        super().__init__()
        self.container: Container = container

    def get_image_name(self) -> str:
        image_name = self.container.attrs.get("Config", {}).get("Image", None)
        if image_name is None:
            raise ObjectNotFoundError("Cannot find image of container: %s" % self.container.name)
        return image_name

    @staticmethod
    def get_container_by_id(container_id: str):
        return DockerContainer(DockerEngine.get_docker().containers.get(container_id))

    @staticmethod
    def get_current_container():
        hostname = socket.gethostname()
        return DockerContainer.get_container_by_id(hostname)


if __name__ == '__main__':
    container = DockerContainer.get_container_by_id("c9edff85d750")
    image = container.get_image_name()
    print(image)
