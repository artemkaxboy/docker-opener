from docker.errors import APIError

from dockerbuild.docker_opener.command import Command
from dockerbuild.docker_opener.docker_engine.docker_engine import DockerEngine
from dockerbuild.docker_opener.image.image import DockerImage
from dockerbuild.docker_opener.system.args import Args

_help_msg = """
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
      port           Temporary forward host port to container
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


class SystemCommand(Command):
    commands = {"help": ["help", "h"], "update": ["update", "u"]}

    def __init__(self, args: Args):
        self.command = SystemCommand.get_command_key(args.get_command())
        self.args = args

    @classmethod
    def get_command_key(cls, command_variable):
        for k, v in cls.commands.items():
            if command_variable in v:
                return k
        raise ValueError("Unknown command: %s" % command_variable)

    @classmethod
    def contains(cls, command):
        for k, v in cls.commands.items():
            if command in v:
                return True

        return False

    def perform(self):

        if self.command == "help":
            self.print_help_message()
        elif self.command == "update":
            self.update()

    @staticmethod
    def print_help_message():
        """
        Prints help message to stdout.
        """
        print(_help_msg)

    @staticmethod
    def update():
        """
        Updates current image tags.
        :return: None
        :raises ValueError cannot find current container image name
        """

        current_image = DockerImage(DockerEngine.get_current_container_image())

        try:
            print("\nPulling %s..." % current_image.get_name())
            current_image.pull()
            print("OK")
        except APIError as e:
            print("error: %s" % e)
