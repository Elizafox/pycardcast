# Copyright © 2015 Elizabeth Myers.
# All rights reserved.
# This file is part of the pycardcast project. See LICENSE in the root
# directory for licensing information.

import abc

from urllib.parse import urlencode

from pycardcast.deck import Deck


__all__ = ["aiohttp", "requests"]


class CardcastAPIBase(metaclass=abc.ABCMeta):
    """The base for all Cardcast network API's."""

    deck_list_max = 50
    """Default maximum number of decks returned in a request."""

    endpoint_url = "https://api.cardcastgame.com/v1/decks"
    """The Cardcast API endpoint."""

    deck_list_url = endpoint_url
    """Endpoint for searching and listing decks."""

    deck_info_url = endpoint_url + "/{code}"
    """Endpoint for getting information on a deck."""

    card_list_url = endpoint_url + "/{code}/cards"
    """Endpoint for getting card listings."""

    @abc.abstractmethod
    def deck_info(self, code):
        """Get the info for the deck with given deck code.

        :param code:
            Code of the deck to retrieve.

        :returns:
            A :py:class:`~pycardcast.deck.DeckInfo` object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def white_cards(self, code):
        """Get the white cards for the deck with the given code.

        :param code:
            code of the deck to retrieve.

        :returns:
            A list of :py:class:`~pycardcast.card.WhiteCard`s.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def black_cards(self, code):
        """Get the black cards for the deck with the given code.

        :param code:
            code of the deck to retrieve.

        :returns:
            A list of :py:class:`~pycardcast.card.BlackCard`s.
        """
        raise NotImplementedError

    def cards(self, code):
        """Get the black and white cards for the deck with given deck code.

        :param code:
            code of the deck to retrieve.

        :returns:
            A tuple containing :py:class:`~pycardcast.card.WhiteCard`s and
            :py:class:`~pycardcast.card.BlackCard`s in two lists.
        """
        return (self.white_cards(code), self.black_cards(code))

    def deck(self, code):
        """Get the deck with the given deck code.

        :param code:
            Code of the deck to retrieve.

        :returns:
            A :py:class:`~pycardcast.deck.Deck` object.
        """
        deckinfo = self.deck_info(code)
        cards = self.cards(code)
        return Deck(deckinfo, cards[0], cards[1])

    @abc.abstractmethod
    def search(self, name=None, author=None, category=None, offset=0,
               limit=deck_list_max):
        """Search for decks matching the given parameters.

        :param name:
            Name of the deck to look for; use ``None`` for any.

        :param author:
            Look for decks by the given author; use ``None`` for any.

        :param category:
            Look for decks in the given category; use ``None`` for any.

        :param offset:
            Offset for pagination of results.

        :param limit:
            Limit the number of results in one query to this.

        :returns:
            A :py:class:`~pycardcast.search.SearchReturn` object.
        """
        raise NotImplementedError

    def search_iter(self, name=None, author=None, category=None, offset=0,
                    limit=deck_list_max):
        """Search for decks matching the given parameters.

        This is similar to search, but is an iterator of search results.

        :param name:
            Name of the deck to look for; use ``None`` for any.

        :param author:
            Look for decks by the given author; use ``None`` for any.

        :param category:
            Look for decks in the given category; use ``None`` for any.

        :param offset:
            Offset for pagination of results.

        :param limit:
            Limit the number of results in one query to this.
        """
        s = self.search(name, author, category, offset, limit)

        while s.count > 0:
            yield s

            offset += s.count
            s = self.search(name, author, category, offset, limit)
