import os
import re

from docker import client, DockerClient
from docker.models.containers import Container, ExecResult

from tools import system_tools

busybox_interpreter = """/tmp/busybox sh -c '
export PATH="/tmp/busybin:$PATH"
echo "Installing busybox..."
export HISTFILE=/dev/null
/tmp/busybox mkdir /tmp/busybin -p
/tmp/busybox --install /tmp/busybin
trap "echo Removing busybox...\nrm -rf /tmp/busybox /tmp/busybin" INT TERM EXIT
sh'"""

compose_project_label = "com.docker.compose.project"
compose_service_label = "com.docker.compose.service"

compose_header = "version: '3.8'\nservices:\n"

fake_compose_path = "/tmp/compose.yml"


def get_container_id(target):
    """
    Returns container's ID by name, image, id, port.
    :param target: known property of wanted container.
    :return: Found container's ID.
    :raises: ValueError if container not found.
    """
    docker = client.from_env()
    containers = docker.containers.list()

    container: Container
    for container in containers:
        if container.name == target:
            print("Found container with name `%s`" % target)
            return container.id

    for container in containers:
        if container.name.find(target) >= 0:
            print("Found container with name containing `%s`" % target)
            return container.id

    for container in containers:
        if ' '.join(container.image.tags).find(target) >= 0:
            print("Found container with image containing `%s`" % target)
            return container.id

    for container in containers:
        if container.id.find(target) >= 0:
            print("Found container with ID containing `%s`" % target)
            return container.id

    for container in containers:
        if target in get_ports(container):
            print("Found container with exposed/mapped port `%s`" % target)
            return container.id

    raise ValueError("Container `%s` not found!" % target)


def get_compose_name(target: str, search_all=False):
    """
    Returns compose's name by it's part
    :param target: known part of name.
    :param search_all: search all containers.
    :return: Found compose's name.
    :raises: ValueError if compose not found.
    """
    docker = client.from_env()
    containers = docker.containers.list(filters={"label": compose_project_label}, all=search_all)

    projects = set(map(lambda container: container.labels[compose_project_label], containers))
    if target in projects:
        print("Found compose with name `%s`" % target)
        return target
    else:
        filtered_projects = list(filter(lambda project: project.find(target) >= 0, projects))
        if filtered_projects:
            target_name = filtered_projects[0]
            print("Found compose with name containing `%s`: %s" % (target, target_name))
            return target_name
        else:
            raise ValueError("Compose not found by name `%s`" % target)


def make_fake_compose(target_name: str, search_all=False):
    """
    Makes fake compose to fetch logs.
    :param target_name: name of compose.
    :return: None
    """
    docker = client.from_env()
    containers = docker.containers.list(filters={"label": compose_project_label + "=" + target_name}, all=search_all)

    with open(fake_compose_path, "w") as file:
        file.write(compose_header)
        container: Container
        for container in containers:
            file.write("  " + container.labels[compose_service_label] + ":\n    build: .\n")


def get_ports(container: Container):
    """
    Returns all exposed and mapped port of the given container as a set.
    :param container: to find port of.
    :return: set of ports.
    """

    ports = set()

    for port in container.ports:
        # adds exposed port
        ports.add(port_to_string(port))

        # find mapped ports
        mapping = container.ports[port]
        found_ports = port_mapping_to_set(mapping)
        ports.update(found_ports)

    return ports


def port_mapping_to_set(raw_port):
    """
    Returns all mapped ports as a set.
    :param raw_port: port in any allowed format
        https://docker-py.readthedocs.io/en/stable/containers.html#container-objects.
    :return: set of ports.
    """

    if raw_port is None:
        return set()

    raw_type = type(raw_port)

    if raw_type is int:
        return {str(raw_port)}

    if raw_type is dict:
        return {port_to_string(raw_port['HostPort'])}

    if raw_type is list:
        result = set()
        for element in raw_port:
            result.update(port_mapping_to_set(element))
        return result


def port_to_string(port):
    """
    Returns clear number string containing port number.
    :param port: port in integer (1234) or string ("1234/tcp") representation.
    :return: port number as number string ("1234").
    """
    port_type = type(port)
    if port_type is int:
        return str(port)
    if port_type is str:
        return re.findall(r"\d+", port)[0]


def get_interpreter(container_id: str):
    """
    Finds available system command interpreter in container or install busybox. Order: bash, sh, busybox.
    :param container_id: target container id to get interpreter.
    :return: interpreter command.
    """
    docker: DockerClient = client.from_env()
    container: Container = docker.containers.get(container_id)

    result: ExecResult = container.exec_run("bash")
    if result.exit_code == 0:
        interpreter = "bash"
    else:
        result: ExecResult = container.exec_run("sh")
        if result.exit_code == 0:
            interpreter = "sh"
        else:
            copy_busybox(container.id)
            interpreter = busybox_interpreter

    return interpreter


def copy_busybox(target_id: str):
    """
    Copies busybox installation file to the target container.
    :param target_id: target container id
    :return: None
    """
    print("Copying busybox...")
    os.system("docker cp /busybox %s:/tmp/busybox" % target_id)


def docker_ps(container_id: str = None, compose_name: str = None, search_all=False):
    """
    Prints docker ps command output.
    :param container_id: prints only given container if given
    :param compose_name: prints only given compose containers if given
    :return: None
    """
    all_command = ["--all"] if search_all else []
    if container_id is None and compose_name is None:
        system_tools.os_run(["docker", "ps"] + all_command)
    elif container_id is not None:
        system_tools.os_run(["docker", "ps", "--filter", "id=" + container_id] + all_command)
    else:
        system_tools.os_run(
            ["docker", "ps", "--filter", "label=" + compose_project_label + "=" + compose_name] + all_command)
