from docker.models.images import Image

from dockerbuild.docker_opener.docker_engine.docker_engine import DockerEngine


class DockerImage:

    def __init__(self, image: Image):
        self.image = image

    def pull(self):
        DockerEngine.get_docker().images.pull(self.get_name())
        pass

    def get_name(self) -> str:
        return self.image.tags[0]

    @staticmethod
    def pull_by_name(image_name: str):
        """

        :param image_name:
        :raises :py:class:`docker.errors.APIError`

        """
        DockerEngine.get_docker().images.pull(image_name)
