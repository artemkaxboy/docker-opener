from errors import ArgumentError, ObjectNotFoundError
from tools import docker_container_tools, docker_common_tools, docker_tools, docker_image_tools, system_tools

connect_command = "docker exec --user 0 -it %s %s"


def shell(args):
    """
    Prepares command to attach to container's shell.

    :param args: array of command args, must have exactly one arg, which is any container's property to connect
    :return: None
    :raises ArgumentError if wrong arguments passed

    :raises ObjectNotFoundError if container not found or more than one container found
    :raises ValueError if container not found or more than one container found
    """
    if len(args) != 1:
        raise ArgumentError("Exactly 1 target required")

    target_id = docker_container_tools.find_container_id(args[0])
    docker_common_tools.docker_ps(container_ids=[target_id])

    interpreter = docker_tools.get_interpreter(target_id)
    print("Connecting...")
    system_tools.prepare_command(connect_command % (target_id, interpreter))


def logs(args):
    """
    Prepares command to fetch container logs.

    Usage:  docker logs [OPTIONS] CONTAINER

    Fetch the logs of a container

    Options:
          --details        Show extra details provided to logs
      -f, --follow         Follow log output
          --since string   Show logs since timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)
      -n, --tail string    Number of lines to show from the end of the logs (default "all")
      -t, --timestamps     Show timestamps
          --until string   Show logs before a timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    try:
        docker_container_tools.docker_command("logs", args)

    except ObjectNotFoundError as e:
        docker_container_tools.docker_command("logs", args, search_all=True)


def attach(args):
    """
    Prepares command to attach to containers.

    Usage:  docker attach [OPTIONS] CONTAINER

    Attach local standard input, output, and error streams to a running container

    Options:
          --detach-keys string   Override the key sequence for detaching a container
          --no-stdin             Do not attach STDIN
          --sig-proxy            Proxy all received signals to the process (default true)

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    docker_container_tools.docker_command("attach", args)


def docker_exec(args):
    """
    Prepares command to exec in containers.

    Usage:  docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

    Run a command in a running container

    Options:
      -d, --detach               Detached mode: run command in the background
          --detach-keys string   Override the key sequence for detaching a container
      -e, --env list             Set environment variables
          --env-file list        Read in a file of environment variables
      -i, --interactive          Keep STDIN open even if not attached
          --privileged           Give extended privileges to the command
      -t, --tty                  Allocate a pseudo-TTY
      -u, --user string          Username or UID (format: <name|uid>[:<group|gid>])
      -w, --workdir string       Working directory inside the container

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    docker_container_tools.docker_command("exec", args, require_command=True)


def inspect(args):
    """
    Prepares command to inspect a container.

    Usage:  docker inspect [OPTIONS] NAME|ID [NAME|ID...]

    Return low-level information on Docker objects

    Options:
      -f, --format string   Format the output using the given Go template
      -s, --size            Display total file sizes if the type is container
          --type string     Return JSON for specified type

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    docker_container_tools.docker_command("inspect", args, allow_multiple_target=True)


def kill(args):
    """
    Prepares command to kill containers.

    Usage:  docker kill [OPTIONS] CONTAINER [CONTAINER...]

    Kill one or more running containers

    Options:
      -s, --signal string   Signal to send to the container (default "KILL")

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    :raises OSError if non interactive mode
    """
    docker_container_tools.docker_command("kill", args, allow_multiple_target=True,
                                          confirm_many="You are killing following containers")


def pause(args):
    """
    Prepares command to pause containers.

    Usage:  docker pause CONTAINER [CONTAINER...]

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    docker_container_tools.docker_command("pause", args, allow_multiple_target=True, allow_options=False,
                                          confirm_many="You are pausing following containers")


def unpause(args):
    """
    Prepares command to unpause containers.

    Usage:  docker unpause CONTAINER [CONTAINER...]

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    docker_container_tools.docker_command("unpause", args, allow_multiple_target=True, allow_options=False,
                                          confirm_many="You are unpausing following containers")


def stop(args):
    """
    Prepares command to stop containers.

    Usage:  docker stop [OPTIONS] CONTAINER [CONTAINER...]

    Stop one or more running containers

    Options:
      -t, --time int   Seconds to wait for stop before killing it (default 10)

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    docker_container_tools.docker_command("stop", args, allow_multiple_target=True,
                                          confirm_many="You are stopping following containers")


def start(args):
    """
    Prepares command to start containers.

    Usage:  docker start [OPTIONS] CONTAINER [CONTAINER...]

    Start one or more stopped containers

    Options:
      -a, --attach               Attach STDOUT/STDERR and forward signals
          --detach-keys string   Override the key sequence for detaching a container
      -i, --interactive          Attach container's STDIN

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    docker_container_tools.docker_command("start", args, allow_multiple_target=True, search_all=True,
                                          confirm_many="You are starting following containers")


def restart(args):
    """
    Prepares command to restart containers.

    Usage:  docker restart [OPTIONS] CONTAINER [CONTAINER...]

    Restart one or more containers

    Options:
      -t, --time int   Seconds to wait for stop before killing the container (default 10)

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    docker_container_tools.docker_command("restart", args, allow_multiple_target=True,
                                          confirm_many="You are restarting following containers")


def rm(args):
    """
    Prepares command to remove containers.

    Usage:  docker rm [OPTIONS] CONTAINER [CONTAINER...]

    Remove one or more containers

    Options:
      -f, --force     Force the removal of a running container (uses SIGKILL)
      -l, --link      Remove the specified link
      -v, --volumes   Remove anonymous volumes associated with the container

    :param args: array of command args, must have attribute to find container at first or last place
    :return: None
    :raises ValueError if no target in args
    """
    docker_container_tools.docker_command("rm", args, allow_multiple_target=True, search_all=True,
                                          confirm_many="You are removing following containers")


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
    target_autoremovable = docker_container_tools.is_container_autoremovable(target_container)
    target_container_image = docker_image_tools.get_image_name(target_container)

    docker_common_tools.docker_ps(container_ids=[target_container_id])

    if need_upgrade:
        docker_image_tools.pull_image(target_container_image)

    print("Recreating `%s` ..." % target_container_name)

    new_container_id = docker_container_tools.copy_container(target_container_id)
    docker_container_tools.stop_container(target_container_id)
    if not target_autoremovable:
        docker_container_tools.remove_container(target_container_id)
    docker_container_tools.rename_container(new_container_id, target_container_name)
    docker_container_tools.start_container(new_container_id)
