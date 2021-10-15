class OpenerBaseException(BaseException):
    """ Any application error. """

    def __init__(self, *args, **kwargs):
        pass


class ArgumentError(OpenerBaseException):
    """ Argument content error. """

    def __init__(self, *args, **kwargs):
        pass


class ObjectNotFoundError(OpenerBaseException):
    """ Object not found error. """

    def __init__(self, *args, **kwargs):
        pass