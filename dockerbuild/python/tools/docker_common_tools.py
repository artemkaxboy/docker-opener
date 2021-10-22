from typing import List

import docker
from docker import DockerClient
from docker.errors import DockerException

from tools.system_tools import os_run

container_label_key = "label"
compose_project_label = "com.docker.compose.project"


def get_docker() -> DockerClient:
    """
    Returns docker client.
    :return: DockerClient from environment
    """
    return docker.client.from_env()


def docker_ps(container_ids: List[str] = None, compose_name: str = None, search_all=False):
    """
    Prints docker ps command output.
    :param container_ids: prints only given containers if any
    :param compose_name: prints only given compose containers if given
    :param search_all: include stopped containers
    :return: None
    """
    all_command = ["--all"] if search_all else []
    if container_ids is None and compose_name is None:
        os_run(["docker", "ps"] + all_command)
    elif container_ids is not None:
        filters = []
        for container_id in container_ids:
            filters.append("--filter")
            filters.append("id=%s" % container_id)
        os_run(["docker", "ps"] + filters + all_command)
    else:
        os_run(
            ["docker", "ps", "--filter", "label=" + compose_project_label + "=" + compose_name] + all_command)


def is_docker_available():
    try:
        docker.client.from_env()
        return True
    except DockerException:
        return False
