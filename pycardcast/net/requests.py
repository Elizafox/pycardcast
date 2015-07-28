# Copyright © 2015 Elizabeth Myers.
# All rights reserved.
# This file is part of the pycardcast project. See LICENSE in the root
# directory for licensing information.

import requests

from pycardcast.net import CardcastAPIBase
from pycardcast.deck import (DeckInfo, DeckInfoNotFoundError,
                             DeckInfoRetrievalError)
from pycardcast.card import (BlackCard, WhiteCard, CardNotFoundError,
                             CardRetrievalError)
from pycardcast.search import (SearchReturn, SearchNotFoundError,
                               SearchRetrievalError)


class CardcastAPI(CardcastAPIBase):
    """A :py:class:`~pycardcast.net.CardcastAPIBase` implementation using the
    requests library."""

    def deck_info(self, code):
        req = requests.get(self.deck_info_url.format(code=code))
        if req.status_code == requests.codes.ok:
            return DeckInfo.from_json(req.json())
        elif req.status_code == requests.codes.not_found:
            err = "Deck not found: {}".format(code)
            raise DeckInfoNotFoundError(err) from req.raise_for_status()
        else:
            err = "Error retrieving deck: {}".format(code)
            raise DeckInfoRetrievalError(err) from req.raise_for_status()

    def white_cards(self, code):
        req = requests.get(self.card_list_url.format(code=code))
        if req.status_code == requests.codes.ok:
            return WhiteCard.from_json(req.json())
        elif req.status_code == requests.codes.not_found:
            err = "White cards not found: {}".format(code)
            raise CardNotFoundError(err) from req.raise_for_status()
        else:
            err = "Error retrieving white cards: {}".format(code)
            raise CardRetrievalError(err) from req.raise_for_status()

    def black_cards(self, code):
        req = requests.get(self.card_list_url.format(code=code))
        if req.status_code == requests.codes.ok:
            return BlackCard.from_json(req.json())
        elif req.status_code == requests.codes.not_found:
            err = "Black cards not found: {}".format(code)
            raise CardNotFoundError(err) from req.raise_for_status()
        else:
            err = "Error retrieving black cards: {}".format(code)
            raise CardRetrievalError(err) from req.raise_for_status()

    def cards(self, code):
        req = requests.get(self.card_list_url.format(code=code))
        if req.status_code == requests.codes.ok:
            json = req.json()
            return (BlackCard.from_json(json), WhiteCard.from_json(json))
        elif req.status_code == requests.codes.not_found:
            err = "Cards not found: {}".format(code)
            raise CardNotFoundError(err) from req.raise_for_status()
        else:
            err = "Error retrieving cards: {}".format(code)
            raise CardRetrievalError(err) from req.raise_for_status()

    def search(self, name=None, author=None, category=None, offset=0,
               limit=None):
        qs = {
            "search": name,
            "author": author,
            "category": category,
            "offset": offset,
            "limit": (deck_list_max if limit is None else limit)
        }
        req = requests.get(self.deck_list_url, params=qs)
        if req.status_code == requests.codes.ok:
            return SearchReturn.from_json(req.json())
        elif req.status_code == requests.codes.not_found:
            err = "Search query returned not found"
            raise SearchNotFoundError(err) from req.raise_for_status()
        else:
            err = "Error searching decks"
            raise SearchRetrievalError(err) from req.raise_for_status()
