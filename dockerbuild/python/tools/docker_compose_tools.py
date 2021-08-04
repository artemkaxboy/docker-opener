from docker.models.containers import Container

from tools.docker_common_tools import get_docker, compose_project_label

compose_service_label = "com.docker.compose.service"

compose_header = "version: '3.8'\nservices:\n"

fake_compose_path = "/tmp/compose.yml"


def get_compose_name(target: str, search_all=False):
    """
    Returns compose's name by it's part
    :param target: known part of name.
    :param search_all: include stopped containers
    :return: Found compose's name
    :raises ValueError if compose not found
    """
    containers = get_docker().containers.list(
        filters={"label": compose_project_label}, all=search_all)

    projects = set(
        map(lambda container: container.labels[compose_project_label], containers))
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
