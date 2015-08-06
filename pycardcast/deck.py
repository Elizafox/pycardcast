# Copyright © 2015 Elizabeth Myers.
# All rights reserved.
# This file is part of the pycardcast project. See LICENSE in the root
# directory for licensing information.

"""Deck related objects. This includes deck-related exception classes
(:py:class:`~pycardcast.deck.DeckInfoNotFoundError` and
:py:class:`~pycardcast.deck.DeckInfoRetrievalError`), the deck metadata
storage class (:py:class:`~pycardcast.deck.DeckInfo`), and the class that
stores metadata and cards (:py:class:`~pycardcast.deck.Deck`).
"""

from collections import namedtuple

from pycardcast.util import isoformat
from pycardcast.card import BlackCard, WhiteCard
from pycardcast import NotFoundError, RetrievalError


Author = namedtuple("Author", "username id")
"""The author of a deck."""

Copyright = namedtuple("Copyright", "external license")
"""The copyright of the deck."""


class DeckInfoNotFoundError(NotFoundError):
    """Given deck info was not found."""


class DeckInfoRetrievalError(RetrievalError):
    """Error retrieving deck info."""


class DeckInfo:
    
    """The class that stores deck-related metadata."""

    def __init__(self, code, name, description, category, blackcount,
                 whitecount, blacksample, whitesample, unlisted, author,
                 copyright, created, updated, rating):
        """Initalise the DeckInfo class.

        :param code:
            The Cardcast 5-alphanumeric code for this deck.

        :param name:
            The name of this deck.

        :param description:
            The description of this deck. May be ``None`` for nonexistent.

        :param category:
            The category this deck is in.

        :param blackcount:
            An integer with the number of black cards in the deck.

        :param whitecount:
            An integer with the number of white cards in the deck.

        :param blacksample:
            A sampling of black cards from the deck. Usually only set for deck
            information returned after a search.

        :param whitesample:
            A sampling of white cards from the deck. Usually only set for deck
            information returned after a search.

        :param unlisted:
            Whether or not this deck is shown in the search listings. Always
            set to ``True`` for decks found in a search.

        :param author:
            A :py:class:`~pycardcast.deck.Author` named tuple that contains
            the author's name and their unique ID.

        :param copyright:
            A :py:class:`~pycardcast.deck.Copyright` named tuple that
            specifies if a copyright is external or not, and if so, where the
            copyright can be found.

        :param created:
            A ``datetime`` object containing the creation date and time of
            this deck.

        :param updated:
            A ``datetime`` object containing the date and time this deck was
            last updated.

        :param rating:
            A ``float`` describing the rating of this deck between 0 and 5.
        """
        self.code = code
        self.name = name
        self.description = description
        self.category = category
        self.blackcount = blackcount
        self.whitecount = whitecount
        self.blacksample = blacksample
        self.whitesample = whitesample
        self.unlisted = unlisted
        self.author = author
        self.copyright = copyright
        self.created = created
        self.updated = updated
        self.rating = rating

    @classmethod
    def from_json(cls, data):
        if "id" in data and data["id"] == "not_found":
            raise DeckInfoNotFoundError(data["message"])

        code = data["code"]
        name = data["name"]
        description = data.get("description", None)
        category = data["category"]

        blackcount = int(data["call_count"])
        whitecount = int(data["response_count"])

        if "sample_calls" in data:
            blacksample = BlackCard.from_json(data["sample_calls"])
        else:
            blacksample = None

        if "sample_responses" in data:
            whitesample = WhiteCard.from_json(data["sample_responses"])
        else:
            whitesample = None

        unlisted = data.get("unlisted", False)

        author = Author(data["author"]["username"], data["author"]["id"])
        copyright = Copyright(data["external_copyright"],
                              data.get("copyright_holder_url", None))

        created = isoformat(data["created_at"])
        updated = isoformat(data["updated_at"])

        rating = float(data["rating"])

        return cls(code, name, description, category, blackcount, whitecount,
                   blacksample, whitesample, unlisted, author, copyright,
                   created, updated, rating)

    def __repr__(self):
        return ("DeckInfo(code={}, name={}, description={}, category={}, "
                "blackcount={}, whitecount={}, blacksample={}, "
                "whitesample={}, unlisted={}, author={}, copyright={}, "
                "created={}, updated={}, rating={})".format(
                    self.code, self.name, self.description, self.category,
                    self.blackcount, self.whitecount, self.blacksample,
                    self.whitesample, self.unlisted, self.author,
                    self.copyright, self.created, self.updated, self.rating))


class Deck:
    
    """A deck object that contains metadata and cards."""

    def __init__(self, deckinfo, blackcards, whitecards):
        """Initalise the deck object.

        :param deckinfo:
            A :py:class:`~pycardcast.deck.DeckInfo` object with the deck's
            metadata.

        :param blackcards:
            A list of :py:class:`~pycardcast.card.BlackCard`s this deck
            contains.

        :param whitecards:
            A list of :py:class:`~pycardcast.card.WhiteCard`s this deck
            contains.
        """
        self.deckinfo = deckinfo
        self.blackcards = blackcards
        self.whitecards = whitecards

    @classmethod
    def from_json(cls, data_deck, data_cards):
        deckinfo = DeckInfo.from_json(data_deck)
        if "calls" in data_cards:
            blackcards = BlackCard.from_json(data_cards["calls"])
        else:
            blackcards = []

        if "responses" in data_cards:
            whitecards = WhiteCard.from_json(data_cards["responses"])
        else:
            whitecards = []

        return cls(deckinfo, blackcards, whitecards)

    def __repr__(self):
        return "Deck(deckinfo={}, blackcards={}, whitecards={})".format(
            self.deckinfo, self.blackcards, self.whitecards)
