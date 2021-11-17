import os

from docker import client, DockerClient
from docker.models.containers import Container, ExecResult

busybox_interpreter = """/bbx/busybox sh -c '
export PATH="/bbx/busybin:$PATH"
echo "Installing busybox..."
export HISTFILE=/dev/null
/bbx/busybox mkdir /bbx/busybin -p
/bbx/busybox --install /bbx/busybin
trap "echo Removing busybox...\nrm -rf /bbx/busybox /bbx/busybin" INT TERM EXIT
sh'"""


def get_interpreter(container_id: str):
    """
    Finds available system command interpreter in container or install busybox. Order: bash, sh, busybox.
    :param container_id: target container id to get interpreter.
    :return: interpreter command
    """
    docker: DockerClient = client.from_env()
    container: Container = docker.containers.get(container_id)

    result: ExecResult = container.exec_run("bash")
    if result.exit_code == 0:
        print("Found native shell: bash")
        interpreter = "bash"
    else:
        result: ExecResult = container.exec_run("sh")
        if result.exit_code == 0:
            print("Found native shell: sh")
            interpreter = "sh"
        else:
            copy_busybox(container.id)
            interpreter = busybox_interpreter

    return interpreter


def copy_busybox(target_id: str):
    """
    Copies busybox installation file to the target container.
    :param target_id: target container id
    :return: None
    """
    print("Copying busybox...")
    os.system("docker cp /bbx %s:/bbx" % target_id)
