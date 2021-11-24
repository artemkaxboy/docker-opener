class Args:
    """
    Holds and work with program arguments.
    """
    args = []

    def __init__(self, args):
        self.args = args

    def is_empty(self):
        """
        :return: true if args non empty, false - otherwise
        """
        return len(self.args) == 0

    def get_command(self):
        if self.is_empty():
            raise ValueError("No command or target passed")

        return self.args[0]
