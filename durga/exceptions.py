class DurgaError(Exception):
    """Main exception class."""
    pass


class ObjectNotFound(DurgaError):
    """The requested object does not exist."""
    pass


class MultipleObjectsReturned(DurgaError):
    """The query returned multiple objects when only one was expected.

    That is, if a get request returns more than one result.
    """
    def __str__(self):
        return 'Your query returned multiple results.'
