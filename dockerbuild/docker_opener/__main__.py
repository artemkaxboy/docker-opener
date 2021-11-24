import sys

from dockerbuild.docker_opener.docker_engine.docker_engine import DockerEngine
from dockerbuild.docker_opener.errors import OpenerBaseException
from dockerbuild.docker_opener.system import utils

if __name__ == '__main__':
    try:
        if not DockerEngine.is_client_available():
            raise OSError("Docker client is not available")

        args = sys.argv[1:]
        # if len(args) == 0:
        #     common.help()
        #     raise ValueError("Command or target required.")
        #
        # command = args[0]
        #
        # if command in help_commands:
        #     common.help()
        # elif command in update_commands:
        #     common.update()
        # elif command in version_commands:
        #     common.version()
        #
        # elif command in compose_down_commands:
        #     compose.down(args[1:])
        # elif command in compose_kill_commands:
        #     compose.kill(args[1:])
        # elif command in compose_list_commands:
        #     compose.clist()
        # elif command in compose_logs_commands:
        #     compose.logs(args[1:])
        # elif command in compose_ps_commands:
        #     compose.ps(args[1:])
        # elif command in compose_start_commands:
        #     compose.start(args[1:])
        # elif command in compose_stop_commands:
        #     compose.stop(args[1:])
        # elif command in compose_top_commands:
        #     compose.top(args[1:])
        #
        # elif command in shell_commands:
        #     container.shell(args[1:])
        # elif command in attach_commands:
        #     container.attach(args[1:])
        # elif command in exec_commands:
        #     container.docker_exec(args[1:])
        # elif command in inspect_commands:
        #     container.inspect(args[1:])
        # elif command in kill_commands:
        #     container.kill(args[1:])
        # elif command in logs_commands:
        #     container.logs(args[1:])
        # elif command in rm_commands:
        #     container.rm(args[1:])
        #
        # elif command in pause_commands:
        #     container.pause(args[1:])
        # elif command in unpause_commands:
        #     container.unpause(args[1:])
        #
        # elif command in stop_commands:
        #     container.stop(args[1:])
        # elif command in start_commands:
        #     container.start(args[1:])
        # elif command in restart_commands:
        #     container.restart(args[1:])
        #
        # elif command in port_commands:
        #     container.open_port(args[1:])
        # elif command in recreate_commands:
        #     container.recreate(args[1:])
        # elif command in upgrade_commands:
        #     container.upgrade(args[1:])
        # else:
        #     container.shell(args)

    except OpenerBaseException as e:
        utils.die("Opener error: " + str(e))
    except (ValueError, OSError) as e:
        utils.die("Opener error: " + str(e))
    except KeyboardInterrupt:
        pass
