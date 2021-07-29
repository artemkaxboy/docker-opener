help_msg = """
Usage: COMMAND [OPTIONS]

Commands:
  --                 Attach terminal to running container
  cd, compose-down   Stop and remove compose resources
  cl, compose-logs   View output from compose containers
  ck, compose-kill   Kill compose containers
      compose-start  Start compose services
      compose-stop   Stop compose services
  ct, compose-top    Display the running compose processes
  h,  help           Show help message
  l,  logs           Fetch container logs
  u,  update         Update (pull) current image

To get more help with opener, check out our docs at https://github.com/artemkaxboy/docker-opener
"""


def run():
    print(help_msg)
