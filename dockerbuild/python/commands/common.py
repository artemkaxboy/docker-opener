import os
import socket

from docker import client
from docker.errors import NotFound, APIError
from docker.models.images import Image

help_msg = """
Usage: COMMAND [OPTIONS]

Commands:
  h,  help           Show help message
  u,  update         Update (pull) current image
  v,  version        Show version

Container commands:
  --                 Attach terminal to running container
  k,  kill           Kill container
  l,  logs           Fetch container logs

Compose commands:
  cd, compose-down   Stop and remove compose resources
  cl, compose-logs   View output from compose containers
  ck, compose-kill   Kill compose containers
      compose-ps     List containers
      compose-start  Start compose services
      compose-stop   Stop compose services
  ct, compose-top    Display the running compose processes

To get more help with opener, check out our docs at https://github.com/artemkaxboy/docker-opener
"""


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
    docker = client.from_env()
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
