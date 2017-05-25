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
