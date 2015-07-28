# Copyright © 2015 Elizabeth Myers.
# All rights reserved.
# This file is part of the pycardcast project. See LICENSE in the root
# directory for licensing information.

import asyncio
import aiohttp

from pycardcast.net import CardcastAPIBase
from pycardcast.deck import (DeckInfo, DeckInfoNotFoundError,
                             DeckInfoRetrievalError)
from pycardcast.card import (BlackCard, WhiteCard, CardNotFoundError,
                             CardRetrievalError)
from pycardcast.search import (SearchReturn, SearchNotFoundError,
                               SearchRetrievalError)


class CardcastAPI(CardcastAPIBase):
    """A :py:class:`~pycardcast.net.CardcastAPIBase` implementation using the
    aiohttp library.

    All the methods here are coroutines except for one:
    :py:meth:`~pycardcast.net.aiohttp.CardcastAPI.search_iter`.
    """

    @asyncio.coroutine
    def deck_info(self, code):
        req = yield from aiohttp.request("get", self.deck_info_url.format
                                         code=code))
        if req.status == 200:
            json=yield from req.json()
            return DeckInfo.from_json(json)
        elif req.status == 404:
            err="Deck not found: {}".format(code)
            raise DeckInfoNotFoundError(err)
        else:
            err="Error retrieving deck: {} (code {})".format(code,
                                                               req.status)
            raise DeckInfoRetrievalError(err)

    @asyncio.coroutine
    def white_cards(self, code):
        req=yield from aiohtp.request("get", self.card_list_url.format(
            code=code))
        if req.status == 200:
            json=yield from req.json()
            return WhiteCard.from_json(json)
        elif req.status == 404:
            err="White cards not found: {}".format(code)
            raise CardNotFoundError(err)
        else:
            err="Error retrieving white cards: {} (code {})".format(
                code, req.status)
            raise CardRetrievalError(err)

    @asyncio.coroutine
    def black_cards(self, code):
        req = yield from aiohtp.request("get", self.card_list_url.format(
            code=code))
        if req.status == 200:
            json = yield from req.json()
            return BlackCard.from_json(json)
        elif req.status == 404:
            err = "Black cards not found: {}".format(code)
            raise CardNotFoundError(err)
        else:
            err = "Error retrieving black cards: {} (code {})".format(
                code, req.status)
            raise CardRetrievalError(err)

    @asyncio.coroutine
    def cards(self, code):
        req = yield from aiohtp.request("get", self.card_list_url.format(
            code=code))
        if req.status == 200:
            json = yield from req.json()
            return (BlackCard.from_json(json), WhiteCard.from_json(json))
        elif req.status == 404:
            err = "Cards not found: {}".format(code)
            raise CardNotFoundError(err)
        else:
            err = "Error retrieving cards: {} (code {})".format(code,
                                                                req.status)
            raise CardRetrievalError(err)

    @asyncio.coroutine
    def deck(self, code):
        deckinfo = yield from self.deck_info(code)
        cards = yield from self.cards(code)
        return Deck(deckinfo, cards[0], cards[1])

    @asyncio.coroutine
    def search(self, name=None, author=None, category=None, offset=0,
               limit=None):
        qs = {
            "search": name,
            "author": author,
            "category": category,
            "offset": offset,
            "limit": (deck_list_max if limit is None else limit)
        }
        req = yield from aiohtp.request("get", self.deck_list_url, params=qs)
        if req.status == 200:
            json = yield from req.json()
            return SearchReturn.from_json(json)
        elif req.status == 404:
            err = "Search query returned not found"
            raise SearchNotFoundError(err)
        else:
            err = "Error searching decks (code {})".format(req.status)
            raise SearchRetrievalError(err)

    def search_iter(self, name=None, author=None, category=None, offset=0,
                    limit=None):
        s = asyncio.async(self.search(name, author, category, offset, limit))

        while s.count > 0:
            yield s

            offset += s.count
            s = asyncio.async(self.search(name, author, category, offset, limit))
