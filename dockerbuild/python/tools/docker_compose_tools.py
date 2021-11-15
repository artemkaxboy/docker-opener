from docker.models.containers import Container

from tools.docker_common_tools import get_docker, compose_project_label, container_label_key, compose_project_dir_label, \
    stack_namespace_label
from tools.docker_container_tools import is_container_running, get_container_name

compose_service_label = "com.docker.compose.service"

compose_header = "version: '3.8'\nservices:\n"

fake_compose_path = "/tmp/compose.yml"


class GroupContainer:
    name: str
    running: bool


class ComposeContainer(GroupContainer):
    project_dir: str
    project_name: str

    def __init__(self, name: str = None, running: bool = False, compose_dir: str = None, project_name: str = None):
        self.name = name
        self.running = running
        self.project_dir = compose_dir
        self.project_name = project_name

    def __str__(self):
        return ("name = %s, running = %s, compose_dir = %s, compose_name = %s" % (
            self.name, self.running, self.project_dir, self.project_name))


class StackContainer(GroupContainer):
    stack_name: str

    def __init__(self, name: str, running: bool, stack_name: str):
        self.name = name
        self.running = running
        self.stack_name = stack_name

    def __str__(self):
        return "name = %s, running = %s, stack_name = %s" % (self.name, self.running, self.stack_name)


def get_compose_containers_list():
    """
    Finds all available compose projects with running/all containers count.
    :return: Dictionary with key - found compose project names, value - array
    [running containers count, all containers count]
    """

    containers = get_composed_containers(search_all=True)

    all_set = {}

    container: Container
    for container in containers:

        project_name = get_compose_project_name(container)
        if project_name is None:
            # Non compose containers
            continue

        container_compose = ComposeContainer(name=container.name, running=is_container_running(container),
                                             compose_dir=get_compose_project_dir(container),
                                             project_name=project_name)

        project_containers = all_set.get(project_name, [])
        project_containers.append(container_compose)
        all_set[project_name] = project_containers

    return all_set


def get_stack_containers_list():
    """
    Finds all available stacks with running/all containers count.
    :return: Dictionary with key - found stack name, value - array
    [running containers count, all containers count]
    """

    containers = get_stacked_containers(search_all=True)

    all_set = {}

    container: Container
    for container in containers:

        stack_name = get_stack_name(container)
        if stack_name is None:
            # Non stack containers
            continue

        stack_container = StackContainer(name=container.name, running=is_container_running(container),
                                         stack_name=stack_name)

        stack_containers = all_set.get(stack_name, [])
        stack_containers.append(stack_container)
        all_set[stack_name] = stack_containers

    return all_set


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
    Returns name of compose project for container if container is created in compose.
    :param container: container to find compose
    :return: compose project name or None
    """
    return container.labels.get(compose_project_label, None)


def get_stack_name(container: Container):
    """
    Returns name of stack for container if container is created in stack.
    :param container: container to find stack name
    :return: stack name or None
    """
    return container.labels.get(stack_namespace_label, None)


def get_compose_project_dir(container: Container):
    """
    Returns dir of compose project for container if container is created in compose.
    :param container: container to find directory
    :return: compose project directory or None
    """
    return container.labels.get(compose_project_dir_label, None)


def get_composed_containers(search_all: bool = True):
    """
    Returns `composed` containers list.
    :param search_all: include stopped container
    :return: `Composed` container list
    """
    return get_docker().containers.list(filters={container_label_key: compose_project_label}, all=search_all)


def get_stacked_containers(search_all: bool = True):
    """
    Returns `stacked` containers list.
    :param search_all: include stopped container
    :return: `Stacked` container list
    """
    return get_docker().containers.list(filters={container_label_key: stack_namespace_label}, all=search_all)
