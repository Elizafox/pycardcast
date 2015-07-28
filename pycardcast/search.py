# Copyright © 2015 Elizabeth Myers.
# All rights reserved.
# This file is part of the pycardcast project. See LICENSE in the root
# directory for licensing information.

from pycardcast import NotFoundError, RetrievalError
from pycardcast.deck import DeckInfo


class SearchNotFoundError(NotFoundError):
    """Search query not found."""


class SearchRetrievalError(RetrievalError):
    """Error retrieving given search."""


class SearchReturn:

    def __init__(self, totaldecks, count, offset, data):
        self.totaldecks = totaldecks
        self.count = count
        self.offset = offset
        self.data = data

    @classmethod
    def from_json(cls, data):
        totaldecks = data["total"]
        results = data["results"]

        count = results["count"]
        offset = results["offset"]
        data = [DeckInfo.from_json(d) for d in results["data"]]

        return cls(totaldecks, count, offset, data)
