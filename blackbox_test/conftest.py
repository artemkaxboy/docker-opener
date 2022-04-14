import docker
import pytest
from docker.models.containers import Container

docker_tag_to_test = 'artemkaxboy/opener:latest'
path_to_docker_build_context = '../dockerbuild'


@pytest.fixture(scope='session')
def no_args_image():
    """ Create a docker image. """
    client = docker.from_env()
    image = client.images.build(path=path_to_docker_build_context, tag=docker_tag_to_test)
    return image


def create_container(image, command):
    """ Create a container from the image and command. """
    volumes = {
        '/var/run/docker.sock': {
            'bind': '/var/run/docker.sock',
            'mode': 'ro',
        }
    }
    client = docker.from_env()
    return client.containers.create(image[0].id, command=command, volumes=volumes)


def start_container(image, command):
    """ Run a container from the image and command. """
    container: Container = create_container(image, command)
    container.start()
    return container


def wait_for_container(image, command):
    """ Wait for a container to exit. """
    container: Container = start_container(image, command)
    return container.wait(), container


def run_container_for_logs(image, command):
    """ Run a container from the image and command, wait for it to exit and return logs. """
    status, container = wait_for_container(image, command)
    logs = get_container_logs(container)
    container.remove()
    return logs


def get_container_logs(container):
    logs = container.logs()
    return logs.decode('utf-8')


def test_capsys(capsys):
    print("hello")
    out, err = capsys.readouterr()
    assert out == "hello\n"
