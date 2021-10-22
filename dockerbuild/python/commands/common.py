import os
import socket

from docker.errors import NotFound, APIError
from docker.models.images import Image

from tools.docker_common_tools import get_docker

help_msg = """
Usage: COMMAND [OPTIONS]

Commands:
  h,  help           Show help message
  u,  update         Update (pull) current image
  v,  version        Show version

Container commands:
  --                 Attach terminal to running container
  a,  attach         Attach local standard input, output, and error streams to a running container
  e,  exec           Run a command in a running container
  i,  inspect        Return low-level information on Docker objects
  k,  kill           Kill containers
  l,  logs           Fetch container logs
  p,  pause          Pause all processes within one or more containers
      recreate       Recreate container
  res,restart        Restart one or more containers
      rm             Remove one or more containers
  sta,start          Start one or more stopped containers
  sto,stop           Stop one or more running containers
      unpause        Unpause all processes within one or more containers
      upgrade        Pull container's image and recreate it

Compose commands:
  cd,  compose-down   Stop and remove compose resources
  ck,  compose-kill   Kill compose containers
       compose-list   Show all compose projects
  cl,  compose-logs   View output from compose containers
  cps, compose-ps     List containers
       compose-start  Start compose services
       compose-stop   Stop compose services
  ct,  compose-top    Display the running compose processes

To get more help with opener, check out our docs at https://github.com/artemkaxboy/docker-opener
"""


# todo - kill confirmation should be positive by default if only one container found

# noinspection PyShadowingBuiltins
def help():
    """
    Prints help message.
    :return: None
    """
    print(help_msg)


def update():
    """
    Updates current image tags.
    :return: None
    :raises ValueError cannot find current container image name
    """
    hostname = socket.gethostname()
    docker = get_docker()
    try:
        current_image: Image = docker.containers.get(hostname).image
    except NotFound:
        raise ValueError("Current container image not found")

    for tag in current_image.tags:
        try:
            print("\nPulling %s..." % tag)
            docker.images.pull(tag)
            print("OK")
        except APIError as e:
            print("error: %s" % e)


def version():
    """
    Prints current image version.
    :return: None
    """
    print("Version: %s" % os.environ.get("VERSION"))
    print("Revision: %s" % os.environ.get("REVISION"))
    print("Created: %s" % os.environ.get("CREATED"))
