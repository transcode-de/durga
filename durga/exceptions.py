class DurgaError(Exception):
    """Main exception class."""
    pass


class ObjectNotFoundError(DurgaError):
    """The requested object does not exist."""
    def __init__(self, request, response):
        self.request = request
        self.response = response


class MultipleObjectsReturnedError(DurgaError):
    """The request returned multiple objects when only one was expected.

    That is, if a GET request returns more than one element.
    """
    def __str__(self):
        return 'Your GET request returned multiple results.'


class ValidationError(DurgaError):
    """The value did not pass the validator."""
    pass
