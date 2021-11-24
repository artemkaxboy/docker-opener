from unittest import TestCase

from dockerbuild.docker_opener.containers.docker_container import DockerContainer


class TestDockerContainer(TestCase):

    def test_get_image_name(self):

        container = DockerContainer.get_container_by_id("b0dd896af26e")
        self.fail()
