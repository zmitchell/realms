"""This module defines the various exceptions raised by realms"""


class RealmsException(Exception):
    """The parent exception from which all other
    realms-specific exceptions are derived
    """
    pass


class DeckEmpty(RealmsException):
    """Raised when attempting to draw a card from an empty deck
    """
    pass


class MainDeckEmpty(DeckEmpty):
    """Raised when attempting to draw a card from the
    main deck when no cards are left
    """
    pass


class PlayerDeckEmpty(DeckEmpty):
    """Raised when attempting to draw a card from the player's
    undrawn pile
    """
    pass


class PlayerDeckInitSize(RealmsException):
    """Raised when attempting to construct a player's deck with the
    wrong number of cards

    Parameters
    ----------
    size : int
        The number of cards that were used to attempt to construct the deck
    """
    def __init__(self, size: int):
        msg = f"Tried to construct deck with {size} cards"
        self.msg = msg


class PlayerDeckInitContents(RealmsException):
    """Raised when attempting to construct a player's deck with cards
    that are not Vipers or Scouts

    Parameters
    ----------
    cardname : str
        The name of the offending card
    """
    def __init__(self, cardname: str):
        msg = f"Deck contained {cardname}"
        self.msg = msg
