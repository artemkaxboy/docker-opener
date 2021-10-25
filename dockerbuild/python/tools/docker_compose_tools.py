from docker.models.containers import Container

from tools.docker_common_tools import get_docker, compose_project_label, container_label_key
from tools.docker_container_tools import is_container_running

compose_service_label = "com.docker.compose.service"

compose_header = "version: '3.8'\nservices:\n"

fake_compose_path = "/tmp/compose.yml"


def get_compose_list():
    """
    Finds all available compose projects with running/all containers count.
    :return: Dictionary with key - found compose project names, value - array
    [running containers count, all containers count]
    """

    containers = get_composed_containers(search_all=True)

    all_set = {}
    running_set = {}

    container: Container
    for container in containers:

        project_name = get_compose_project_name(container)
        if project_name is None:
            # Non compose containers
            continue

        all_set[project_name] = all_set.get(project_name, 0) + 1
        if is_container_running(container):
            running_set[project_name] = running_set.get(project_name, 0) + 1

    # create set key: project_name, value: [running count, all count]
    result_set = dict(map(lambda kv: (kv[0], [running_set.get(kv[0], 0), kv[1]]), all_set.items()))
    return result_set


def get_compose_name(target: str, search_all=False):
    """
    Returns compose's name by it's part
    :param target: known part of name.
    :param search_all: include stopped containers
    :return: Found compose's name
    :raises ValueError if compose not found
    """
    containers = get_composed_containers(search_all=search_all)

    # make set of compose projects
    projects = set(map(lambda container: get_compose_project_name(container), containers))

    if target in projects:
        print("Found compose with name `%s`" % target)
        return target
    else:
        filtered_projects = list(
            filter(lambda project: project.find(target) >= 0, projects))
        if filtered_projects:
            target_name = filtered_projects[0]
            print("Found compose with name containing `%s`: %s" %
                  (target, target_name))
            return target_name
        else:
            raise ValueError("Compose not found by name `%s`" % target)


def make_fake_compose(target_name: str, search_all=False):
    """
    Makes fake compose to fetch logs.
    :param target_name: name of compose.
    :param search_all: include stopped containers
    :return: None
    """
    containers = get_docker().containers.list(
        filters={"label": compose_project_label + "=" + target_name}, all=search_all)

    with open(fake_compose_path, "w") as file:
        file.write(compose_header)
        container: Container
        for container in containers:
            file.write(
                "  " + container.labels[compose_service_label] + ":\n    build: .\n")


def get_compose_project_name(container: Container):
    """
    Returns name of compose project for container if container is running in compose.
    :param container: container to find compose
    :return: compose project name or None
    """
    return container.labels.get(compose_project_label, None)


def get_composed_containers(search_all: bool = True):
    """
    Returns `composed` containers list.
    :param search_all: include stopped container
    :return: `Composed` container list
    """
    return get_docker().containers.list(filters={container_label_key: compose_project_label}, all=search_all)
