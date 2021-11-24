from dockerbuild.docker_opener.command import Command


class ContainerCommand(Command):
    """ Opener container command to run """

    commands = { }

    shell_commands = ["--"]
    attach_commands = ["a", "attach"]
    exec_commands = ["e", "exec"]
    inspect_commands = ["i", "inspect"]
    kill_commands = ["k", "kill"]
    logs_commands = ["l", "logs"]
    rm_commands = ["rm"]

    pause_commands = ["p", "pause"]
    unpause_commands = ["un", "unpause"]

    stop_commands = ["sto", "stop"]
    start_commands = ["sta", "start"]
    restart_commands = ["res", "restart"]

    port_commands = ["port"]
    recreate_commands = ["recreate"]
    upgrade_commands = ["upgrade"]

