class InvalidValueError(Exception):
    """docstring for InvalidValueError."""
    def __init__(self, message):
        super(InvalidValueError, self).__init__(message)
