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
from .exceptions import (
    RealmsException,
    MainDeckEmpty,
    PlayerDeckEmpty,
    PlayerDeckInitSize,
    PlayerDeckInitContents
)

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
    shuffles the deck when necessary.

    Parameters
    ----------
    player_cards : List[Card]
        The list of cards from which the player's starting deck will be constructed

    Raises
    ------
    PlayerDeckInitSize
        Raised when constructing the deck with the wrong number of cards
    PlayerDeckInitContents
        Raised when constructing the deck with cards other than Vipers and Scouts
    """

    starting_size = 10

    def __init__(self, player_cards: CardList):
        try:
            self._validate_deck_size(player_cards)
            self._validate_deck_contents(player_cards)
        except RealmsException:
            raise
        self._undrawn: CardList = player_cards
        shuffle(self._undrawn)  # shuffled in place
        self._discards: CardList = []

    @staticmethod
    def _validate_deck_size(cards: CardList) -> None:
        """Ensures that the starting deck contains the correct
        number of cards

        Parameters
        ----------
        cards : CardList
            The tentative starting deck

        Raises
        ------
        PlayerDeckInitSize
            Raised if the tentative starting deck is not the correct size
        """
        if len(cards) != PlayerDeck.starting_size:
            raise PlayerDeckInitSize(len(cards))
        return

    @staticmethod
    def _validate_deck_contents(cards) -> None:
        """Ensures that the tentative starting deck contains only Vipers and Scouts

        Parameters
        ----------
        cards : CardList
            The tentative starting deck

        Raises
        ------
        PlayerDeckInitContents
            Raised if the tentative starting deck contains cards other than Vipers or Scouts
        """
        for c in cards:
            if (c.name != 'Viper') and (c.name != 'Scout'):
                raise PlayerDeckInitContents(c.name)
        return

    def _next_card(self) -> Card:
        """Produces the next card from the player's deck

        Attempts to draw a card from the top of the undrawn pile. If
        the undrawn pile is empty, the undrawn pile is replenished from
        the discard pile and shuffled before attempting to draw a card again.
        An attempt to draw a card from the undrawn pile while both the undrawn
        pile and discard pile are empty will raise a ``PlayerDeckEmpty`` exception.

        Returns
        -------
        Card
            A card from the top of the undrawn pile

        Raises
        ------
        PlayerDeckEmpty
            Raised when attempting to draw a card while both undrawn and discard
            piles are empty
        """
        if len(self._undrawn) > 0:
            return self._undrawn.pop()
        elif len(self._discards) > 0:
            self._refill_undrawn()
            return self._undrawn.pop()
        else:
            raise PlayerDeckEmpty

    def _refill_undrawn(self) -> None:
        """Refills the undrawn pile with cards from the discard pile

        Note
        ----
        The cards in the discard pile are shuffled before being placed
        back into the undrawn pile
        """
        self._undrawn: CardList = self._discards
        shuffle(self._undrawn)  # shuffled in place
        self._discards: CardList = []
        return

    def discard(self, card: Card) -> None:
        """Sends the card to the discard pile

        Parameters
        ----------
        card : Card
            The card to send to the discard pile
        """
        self._discards.append(card)
        return

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
