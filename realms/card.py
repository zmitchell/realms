# -*- coding: utf-8 -*-
"""
.. module:: card
    :synopsis: Encapsulate card behavior
.. moduleauthor:: Zach Mitchell <zmitchell@fastmail.com>
"""

from enum import Enum


class Card(object):
    """ Represents a card in the game

    Parameters
    ----------
    uuid : UUID
        A unique identifier for the card
    name : str
        The display name of the card
    is_base : bool
        Denotes whether the card is a base or a ship
    is_outpost : bool
        If the card is a base, this denotes whether it is also an outpost
    health : int
        If the card is a base, this is the amount of damage required to destroy it
    cost : int
        The cost to buy the card
    faction : CardFaction
        The faction to which the card belongs
    effects : [CardEffect]
        A list of effects provided by the card
    ally_abilities : [CardEffect]
        A list of effects activated by cards of the same faction
    image
        The display image of the card

    Note
    ----
    The constructor for this class will likely be overhauled to simply take
    an instance of ``CardPrimitive`` and a few other parameters to simplify
    the process of constructing a ``Card``.
    """

    def __init__(self, uuid, name, is_base=False, is_outpost=False, health=None,
                 cost=None, faction=None, effects=None, ally_ability=None, image=None):
        pass


class CardFaction(Enum):
    """The set of allowed card factions

    Warning
    -------
    Take care when dealing with ``CardFaction`` and ``FactionPrimitive`` instances.
    The ``name`` attribute of ``FactionPrimitive`` is of the form "Star Empire",
    whereas the ``name`` attribute of an Enum subclass refers to the name of the
    Enum member i.e. "STAR" in the case of ``CardFaction.STAR``.
    """

    ALL = 'All'
    """A card, such as Machine Base, that triggers ally abilities for all factions
    """
    BLOB = 'Blob'
    FEDERATION = 'Federation'
    MACHINE = 'Machine Cult'
    STAR = 'Star Empire'
    UNALIGNED = 'Unaligned'
    """A card with no faction, such as Viper, Scout, or Explorer
    """

    @classmethod
    def from_primitive(cls, primitive):
        """Creates the corresponding ``CardFaction`` instance from a
        ``FactionPrimitive`` instance
        """
        return next(f for f in cls if f.value == primitive.name)

    def __str__(self):
        """
        Display string representation of the faction

        Returns
        -------
        str
            The display-ready string representation of the faction

        Examples
        --------
        >>> fac = CardFaction.STAR
        >>> str(fac)
        Star Empire
        """
        return self.value


class CardEffect(object):
    """A single effect provided by a card

    Identifies an action, any values associated with the action,
    and who the effect should be applied to.

    Parameters
    ----------
    target : CardTarget
        The player who should receive the effect of the card
    action : CardAction
        The type of action to apply
    value : int
        The value associated with the action
    """
    def __init__(self, target, action, value):
        self.target = target
        self.action = action
        self.value = value
        return


class CardTarget(Enum):
    """The receiver of a card's effect
    """
    OPPONENT = 0
    OWNER = 1


class CardAction(Enum):
    """The type of action that an effect entails
    """
    ATTACK = 0
    """Reduce the target's health"""
    ACQUIRE = 1
    """Buy a card without paying its cost"""
    DESTROY = 2
    """Destroy a target base without spending any attack power"""
    DISCARD = 3
    """The target sends a card from his hand to his discard pile"""
    DRAW = 4
    """Draw cards from the player's deck"""
    HEAL = 5
    """Increase the player's health"""
    MONEY = 6
    """Provides currency with which to buy cards"""
    SCRAP = 7
    """Permanently discard a card"""



