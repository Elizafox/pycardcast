# COPYRIGHT


class PycardcastError(Exception):
    """Base exception for pycardcast errors."""


class RetrievalError(PycardcastError):
    """Error retrieving the given object or resource."""


class NotFoundError(RetrievalError):
    """The given object or resource doesn't exist."""


