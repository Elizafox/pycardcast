# Copyright © 2015 Elizabeth Myers.
# All rights reserved.
# This file is part of the pycardcast project. See LICENSE in the root
# directory for licensing information.

"""Various card-related structures. The most interesting parts to most
developers are likely to be :py:class:`~pycardcast.card.BlackCard` and
:py:class:`~pycardcast.card.WhiteCard`.
"""

from pycardcast.util import isoformat
from pycardcast import NotFoundError, RetrievalError


class CardNotFoundError(NotFoundError):
    """Card or cards were not found."""


class CardRetrievalError(RetrievalError):
    """Error retrieving card or cards."""


class Card:
    """The base card object."""

    def __init__(self, created, cid, text):
        """Create a card object.

        :param created:
            a ``datetime`` object representing when the card was created.

        :param cid:
            The unique ID of the card.

        :param text:
            The text on the face of the card.
        """
        self.created = created
        self.cid = cid
        self.text = text


class BlackCard(Card):
    """A black card object."""
    def __init__(self, created, cid, text, pick=None):
        """Create a blackcard object.

        :param created:
            a ``datetime`` object representing when the card was created.

        :param cid:
            The unique ID of the card.

        :param text:
            The text on the face of the card.

        :param pick:
            How many white cards are picked for this card.
        """
        # Remove blanks
        if pick is None:
            self.pick = len(text) - 1
            if self.pick == 0:
                # This shouldn't happen...
                self.pick = 1
        else:
            self.pick = pick

        # Avoid "foo?_____" problem
        if text[-1] == '' and text[-2][-1] != ' ':
            text.pop()

        text = "_____".join(filter(None, text))

        super().__init__(created, cid, text)

    @classmethod
    def from_json(cls, data):
        if "calls" in data:
            return [cls.from_json(c) for c in data["calls"]]

        if data["id"] == "not_found":
            raise CardNotFoundError(data["message"])

        return cls(isoformat(data["created_at"]), data["id"], data["text"])

    def __hash__(self):
        return hash((self.pick, self.created, self.cid, self.text)) + 1

    def __repr__(self):
        return "BlackCard(created={}, cid={}, text={}, pick={})".format(
            self.created, self.cid, self.text, self.pick)


class WhiteCard(Card):
    """A white card object."""

    @classmethod
    def from_json(cls, data):
        if "responses" in data:
            return [cls.from_json(c) for c in data["responses"]]

        if data["id"] == "not_found":
            raise CardNotFoundError(data["message"])

        return cls(isoformat(data["created_at"]), data["id"], data["text"])

    def __hash__(self):
        return hash((self.created, self.cid, self.text)) - 1

    def __repr__(self):
        return "WhiteCard(created={}, cid={}, text={})".format(
            self.created, self.cid, self.text)
