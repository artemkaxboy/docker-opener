from tools import docker_container_tools, docker_common_tools, docker_tools, docker_image_tools, system_tools

connect_command = "docker exec --user 0 -it %s %s"


def attach(args):
    """
    Prepares command to attach to container.
    :param args: array of command args, must have exactly one arg, which is any container's property to connect
    :return: None
    :raises ValueError if no or more than one target in args
    """
    if len(args) != 1:
        raise ValueError("Exactly 1 target required")

    target_id = docker_container_tools.find_container_id(args[0])
    docker_common_tools.docker_ps(container_ids=[target_id])

    interpreter = docker_tools.get_interpreter(target_id)
    print("Connecting...")
    system_tools.prepare_command(connect_command % (target_id, interpreter))


def logs(args):
    """
    Prepares command to fetch container logs.
    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    if len(args) == 0:
        raise ValueError("Logs target required")

    target, options = system_tools.divide_target_and_options(args)
    target_id = docker_container_tools.find_container_id(target)
    docker_common_tools.docker_ps(container_ids=[target_id])

    system_tools.prepare_command("docker logs %s %s" % (target_id, options))


def kill(args):
    """
    Prepares command to kill containers.
    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    :raises OSError if non interactive mode
    """
    if len(args) == 0:
        raise ValueError("Kill target required")

    target, options = system_tools.divide_target_and_options(args)
    target_container_ids = docker_container_tools.find_container_ids(target, raise_if_not_found=True)

    docker_common_tools.docker_ps(container_ids=target_container_ids)

    if system_tools.get_consent("You are killing %d container(s)" % len(target_container_ids)):
        commands = '\n'.join(map(lambda target_id: "docker kill %s %s" %
                                                   (target_id, options), target_container_ids))
        system_tools.prepare_command(commands)


def upgrade(args):
    """
    Recreates container with existing parameters and prepares command to start the new one.
    Pulls image before recreating.
    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    :raises OSError if non interactive mode
    """
    recreate(args, need_upgrade=True)


def recreate(args, need_upgrade: bool = False):
    """
    Recreates container with existing parameters and prepares command to start the new one.
    :param need_upgrade: pull image before recreating
    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args, if no target or more than one target found
    :raises OSError if non interactive mode
    """
    if len(args) == 0:
        raise ValueError("Recreate target required")

    if len(args) != 1:
        raise ValueError("Command has no options")

    target_container = docker_container_tools.find_container(args[0])
    target_container_id = target_container.id
    target_container_name = target_container.name
    target_container_image = docker_image_tools.get_image_name(target_container)

    docker_common_tools.docker_ps(container_ids=[target_container_id])

    if need_upgrade:
        docker_image_tools.pull_image(target_container_image)

    print("Recreating `%s` ..." % target_container_name)

    new_container_id = docker_container_tools.copy_container(target_container_id)
    docker_container_tools.stop_container(target_container_id)
    docker_container_tools.remove_container(target_container_id)
    docker_container_tools.rename_container(new_container_id, target_container_name)
    docker_container_tools.start_container(new_container_id)
