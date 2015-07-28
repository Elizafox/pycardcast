# COPYRIGHT

from collections import namedtuple

from pycardcast.util import isoformat
from pycardcast.card import BlackCard, WhiteCard
from pycardcast import NotFoundError, RetrievalError


Author = namedtuple("Author", "username id")
Copyright = namedtuple("Copyright", "external license")


class DeckInfoNotFoundError(NotFoundError):
    """Given deck info was not found."""


class DeckInfoRetrievalError(RetrievalError):
    """Error retrieving deck info."""


class DeckInfo:

    def __init__(self, code, name, description, category, blackcount,
                 whitecount, blacksample, whitesample, unlisted, author,
                 copyright, created, updated, rating):
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


class Deck:

    def __init__(self, deckinfo, blackcards, whitecards):
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
