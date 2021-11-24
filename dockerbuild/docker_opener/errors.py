class OpenerBaseException(Exception):
    """ Any application error """


class ArgumentError(OpenerBaseException):
    """ Argument content error """


class ObjectNotFoundError(OpenerBaseException):
    """ Object not found error """
