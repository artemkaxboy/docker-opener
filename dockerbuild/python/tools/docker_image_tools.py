from docker.models.containers import Container

from tools import docker_container_tools
from tools.docker_common_tools import get_docker


def get_image_name(container: Container):
    return container.attrs['Config']['Image']


def pull_image(image_name: str):
    print("Pulling image `%s`..." % image_name)
    get_docker().images.pull(image_name)


def pull_image_for_container(container_id: str):
    get_image_name(docker_container_tools.get_container(container_id))
