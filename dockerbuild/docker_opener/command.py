class Command:
    """ Opener command to run """

    @classmethod
    def contains(cls, command):
        raise NotImplementedError("Method is not implemented")

    @classmethod
    def get_command_key(cls, command):
        raise NotImplementedError("Method is not implemented")

    def perform(self):
        raise NotImplementedError("Method is not implemented")
