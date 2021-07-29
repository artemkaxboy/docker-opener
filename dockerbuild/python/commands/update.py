import socket

import docker
from docker.errors import APIError, NotFound
from docker.models.images import Image


def run():
    hostname = socket.gethostname()
    client = docker.from_env()
    try:
        current_image: Image = client.containers.get(hostname).image
    except NotFound:
        raise ValueError("Current container image not found")

    for tag in current_image.tags:
        try:
            print("\nPulling %s..." % tag)
            client.images.pull(tag)
            print("OK")
        except APIError as e:
            print("error: %s" % e)
