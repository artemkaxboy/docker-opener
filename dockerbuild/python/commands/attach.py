from tools import docker_tools
from tools import system_tools

connect_command = "docker exec --user 0 -it %s %s"


def run(args):
    """
    Attaches to container.
    :param args: array of command args, must have exactly one arg, which is any container's property to connect
    :return: None
    """
    if len(args) != 1:
        system_tools.die("Exactly 1 target required")

    target_id = docker_tools.get_container_id(args[0])
    docker_tools.docker_ps(target_id)

    interpreter = docker_tools.get_interpreter(target_id)
    print("Connecting...")
    system_tools.prepare_command(connect_command % (target_id, interpreter))
