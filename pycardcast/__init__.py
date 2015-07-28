# Copyright © 2015 Elizabeth Myers.
# All rights reserved.
# This file is part of the pycardcast project. See LICENSE in the root
# directory for licensing information.


class PycardcastError(Exception):
    """Base exception for pycardcast errors."""


class RetrievalError(PycardcastError):
    """Error retrieving the given object or resource."""


class NotFoundError(RetrievalError):
    """The given object or resource doesn't exist."""
