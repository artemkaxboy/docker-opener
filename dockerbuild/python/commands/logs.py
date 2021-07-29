from tools import docker_tools
from tools import system_tools


def run(args):
    if len(args) == 0:
        system_tools.die("Logs target required")

    target, options = system_tools.divide_target_and_options(args)
    target_id = docker_tools.get_container_id(target)
    docker_tools.docker_ps(container_id=target_id)

    system_tools.os_run(["docker", "logs", target_id] + options)
