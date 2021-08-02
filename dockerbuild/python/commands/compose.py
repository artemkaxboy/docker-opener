from tools import system_tools
from tools.docker_tools import docker_ps, get_compose_name, make_fake_compose, fake_compose_path

compose_project = "docker-compose --project-name %s --file "
compose_logs_command = compose_project + fake_compose_path + " logs %s"
compose_kill_command = compose_project + fake_compose_path + " kill %s"
compose_down_command = compose_project + fake_compose_path + " down %s"
compose_start_command = compose_project + fake_compose_path + " start %s"
compose_stop_command = compose_project + fake_compose_path + " stop %s"
compose_top_command = compose_project + fake_compose_path + " top %s"


def prepare_command(args, command, search_all=False):
    if len(args) == 0:
        system_tools.die("Target required")

    target = args[0]

    target_name = get_compose_name(target, search_all)
    docker_ps(compose_name=target_name, search_all=search_all)

    make_fake_compose(target_name, search_all=search_all)
    arg_string = ' '.join(args[1:])
    system_tools.prepare_command(command % (target_name, arg_string))


def logs(args):
    if len(args) == 0:
        system_tools.die("Compose logs target required")

    prepare_command(args, compose_logs_command, search_all=True)


def kill(args):
    if len(args) == 0:
        system_tools.die("Compose kill target required")

    prepare_command(args, compose_kill_command)


def down(args):
    if len(args) == 0:
        system_tools.die("Compose down target required")

    prepare_command(args, compose_down_command, search_all=True)


def start(args):
    if len(args) == 0:
        system_tools.die("Compose start target required")

    prepare_command(args, compose_start_command, search_all=True)


def stop(args):
    if len(args) == 0:
        system_tools.die("Compose stop target required")

    prepare_command(args, compose_stop_command)


def top(args):
    if len(args) == 0:
        system_tools.die("Compose top target required")

    prepare_command(args, compose_top_command)
