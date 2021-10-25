from tools import system_tools
from tools.docker_common_tools import docker_ps
from tools.docker_compose_tools import fake_compose_path, get_compose_name, make_fake_compose, \
    get_compose_containers_list, ComposeContainer

compose_project = "docker-compose --project-name %s --file "
compose_logs_command = compose_project + fake_compose_path + " logs %s"
compose_kill_command = compose_project + fake_compose_path + " kill %s"
compose_down_command = compose_project + fake_compose_path + " down %s"
compose_ps_command = compose_project + fake_compose_path + " ps %s"
compose_start_command = compose_project + fake_compose_path + " start %s"
compose_stop_command = compose_project + fake_compose_path + " stop %s"
compose_top_command = compose_project + fake_compose_path + " top %s"


def prepare_command(args, command, search_all=False):
    """
    Prepares compose command to run.
    :param args: array of command args, must have attribute to find compose at first place
    :param command: command to prepare
    :param search_all: include stopped containers
    :return: None
    :raises ValueError if no target found
    """
    if len(args) == 0:
        raise ValueError("Target required")

    target = args[0]

    target_name = get_compose_name(target, search_all)
    docker_ps(compose_name=target_name, search_all=search_all)

    make_fake_compose(target_name, search_all=search_all)
    arg_string = ' '.join(args[1:])
    system_tools.prepare_command(command % (target_name, arg_string))


def clist():
    """
    Prints all available compose projects with running/all containers count and compose directories.
    :return: None
    """
    print("All available compose projects (running containers/all containers):")
    for project_stat in get_compose_containers_list().items():

        compose_container: ComposeContainer

        running_containers_count = sum(1 for compose_container in project_stat[1] if compose_container.running)
        all_containers_count = len(project_stat[1])
        compose_project_name = project_stat[0]

        print("\n  - %s: %d/%d" % (compose_project_name, running_containers_count, all_containers_count))

        compose_project_dirs = set(
            map(lambda compose_container_inner: compose_container_inner.project_dir, project_stat[1]))
        print("    compose directories:")
        for compose_project_dir in compose_project_dirs:
            print("    - %s" % compose_project_dir)


def logs(args):
    """
    Prepare compose logs command.
    :param args: array of command args, must have attribute to find compose at first place
    :return: None
    :raises ValueError if no target found
    """
    if len(args) == 0:
        raise ValueError("Compose logs target required")

    prepare_command(args, compose_logs_command, search_all=True)


def kill(args):
    """
    Prepare compose kill command.
    :param args: array of command args, must have attribute to find compose at first place
    :return: None
    :raises ValueError if no target found
    """
    if len(args) == 0:
        raise ValueError("Compose kill target required")

    prepare_command(args, compose_kill_command)


def down(args):
    """
    Prepare compose down command.
    :param args: array of command args, must have attribute to find compose at first place
    :return: None
    :raises ValueError if no target found
    """
    if len(args) == 0:
        raise ValueError("Compose down target required")

    prepare_command(args, compose_down_command, search_all=True)


def start(args):
    """
    Prepare compose start command.
    :param args: array of command args, must have attribute to find compose at first place
    :return: None
    :raises ValueError if no target found
    """
    if len(args) == 0:
        raise ValueError("Compose start target required")

    prepare_command(args, compose_start_command, search_all=True)


def stop(args):
    """
    Prepare compose stop command.
    :param args: array of command args, must have attribute to find compose at first place
    :return: None
    :raises ValueError if no target found
    """
    if len(args) == 0:
        raise ValueError("Compose stop target required")

    prepare_command(args, compose_stop_command)


def top(args):
    """
    Prepare compose top command.
    :param args: array of command args, must have attribute to find compose at first place
    :return: None
    :raises ValueError if no target found
    """
    if len(args) == 0:
        raise ValueError("Compose top target required")

    prepare_command(args, compose_top_command)


def ps(args):
    """
    Prepare compose ps command.
    :param args: array of command args, must have attribute to find compose at first place
    :return: None
    :raises ValueError if no target found
    """
    if len(args) == 0:
        raise ValueError("Compose ps target required")

    prepare_command(args, compose_ps_command, search_all=True)
