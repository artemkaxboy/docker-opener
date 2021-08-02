from tools import docker_tools
from tools import system_tools

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

    target_id = docker_tools.get_container_id(args[0])
    docker_tools.docker_ps(target_id)

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
    target_id = docker_tools.get_container_id(target)
    docker_tools.docker_ps(container_id=target_id)

    system_tools.prepare_command("docker logs %s %s" % (target_id, options))
