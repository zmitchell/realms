# -*- coding: utf-8 -*-
"""
.. module:: deck
    :synopsis: Encapsulates the behavior of card collections
.. moduleauthor:: Zach Mitchell <zmitchell@fastmail.com>
"""

from random import shuffle
from typing import List
from .cards import Card
from .cardrepo import CardRepo
from .exceptions import MainDeckEmpty

CardList = List[Card]


class Hand(object):
    """
    The player's hand of cards

    Contains a collection of cards, each of which provides one or more effects.
    Some cards may be bases, and thus will not be discarded after being played.

    :param cards: Cards drawn by the player
    :type cards: [Card]
    :param existing_bases: Bases that were played previously and have not been destroyed
    :type existing_bases: [Card]

    .. note:: INCOMPLETE
    """
    def __init__(self, cards, existing_bases):
        self._cards = cards
        self._existing_bases = existing_bases
        self._effects = self._aggregate_effects(self._cards + self._existing_bases)
        return

    def _aggregate_effects(self, cards):
        """
        Returns a list of effects provided by a list of cards

        Examines each card and extracts the relevant effects that it provides.
        Ally abilities are extracted if allies exist in the hand of cards.

        :param cards: The cards whose effects will be aggregated
        :type cards: [Card]
        :return A list of effects provided by the cards
        :rtype [CardEffect]
        """
        pass

    def _factions_with_allies(self, cards):
        """
        Returns a list of factions that appear more than once in the hand

        :param cards: The cards to check for allies
        :type cards: [Card]
        :return A list of factions with allies present in the hand
        :rtype [Faction]
        """
        pass

    def _scrap(self, card):
        """
        Permanently removes a card from the player's deck

        :param card: The card to permanently remove
        :type card: Card
        """
        pass


class PlayerDeck(object):
    """
    Records the state of the player's deck

    At any given point in time the player may have three piles of cards: undrawn cards, a
    hand of cards, and a pile of used (discarded) cards. PlayerDeck records which cards are
    in which pile, provides an interface from which a hand of cards can be assembled, and
    shuffles the deck when necessary. All players begin with the same deck, so no input
    is required to construct a PlayerDeck.
    """
    def __init__(self):
        self.discards = self._initialize_deck()

    @staticmethod
    def _initialize_deck():
        """
        Returns the deck that every player starts with

        :return A deck containing 8 Scouts and 2 Vipers
        :rtype [Card]
        """
        pass

    def _discard(self, card):
        """
        Sends a card to the discard pile

        :param card: The card to discard
        :type card: Card
        """
        pass

    def draw(self, num=5):
        """
        Draws the specified number of cards

        :return A list containing the specified number of cards
        :rtype [Card]
        """
        pass

    def _scrap(self, card):
        """
        Permanently removes a card from the discard pile
        """
        pass


class MainDeck(object):
    """The deck from which players can acquire cards

    Parameters
    ----------
    cardrepo : CardRepo
        The repository from which the cards are obtained
    """
    def __init__(self, cardrepo: CardRepo):
        self._repo: CardRepo = cardrepo
        self._cards: CardList = self._repo.main_deck_cards()
        shuffle(self._cards)
        return

    def next_card(self) -> Card:
        """Produces the next card from the main deck

        Returns
        -------
        Card
            A card from the top of the main deck

        Raises
        ------
        MainDeckEmpty
            Raised when attempting to draw a card when the deck is empty
        """
        if len(self._cards) > 0:
            return self._cards.pop()
        else:
            raise MainDeckEmpty


class TradeRow(object):
    """Presents the cards that players may acquire

    Parameters
    ----------
    maindeck : MainDeck
        The deck from which the trade row is drawn
    cardrepo : CardRepo
        The repository from which cards are obtained
    """
    def __init__(self, maindeck: MainDeck, cardrepo: CardRepo):
        self._maindeck: MainDeck = maindeck
        self._repo: CardRepo = cardrepo

    def scrap(self, card):
        """
        Permanently removes a card from the trade row
        """
        pass

    def add_card(self, card):
        """
        Adds a card to the trade row
        """
        pass

    def make_explorer(self):
        """
        Generates a new Explorer card
        """
        pass
