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
    card_primitive : CardPrimitive
        A CardPrimitive instance from the ORM to convert into a Card
    uuid : UUID
        A unique identifier to assign to the card

    Attributes
    ----------
    uuid : UUID
        A unique identifier for this instance of this card
    name : str
        A display name for the card
    faction : CardFaction
        The faction to which the card belongs
    base : bool
        Is the card a base
    outpost : bool
        If the card is a base, is it also an outpost
    defense : int
        If the card is a base, the amount of damage required to destroy it
    cost : int
        The amount of trade needed to acquire the card
    effects_basic : [CardEffect]
        The effects activated when the card is played
    effects_ally : [CardEffect]
        The effects activated by other cards of the same faction
    effects_scrap : [CardEffect]
        The effects activated when the player chooses to scrap the card

    Note
    ----
    Different instances of a single card i.e. different Vipers will have
    different UUIDs
    """
    def __init__(self, card_primitive, uuid):
        self.uuid = uuid
        self.name = card_primitive.name
        self.faction = CardFaction.from_primitive(card_primitive.faction)
        self.base = card_primitive.base
        self.outpost = card_primitive.outpost
        self.defense = card_primitive.defense
        self.cost = card_primitive.cost
        self.effects_basic = [CardEffect(e) for e in card_primitive.effects]
        self.effects_ally = [CardEffect(e) for e in card_primitive.ally]
        self.effects_scrap = [CardEffect(e) for e in card_primitive.scrap]
        return


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

    Attributes
    ----------
    target : CardTarget
        The player who should receive the effect of the card
    action : CardAction
        The type of action to apply
    value : int
        The value associated with the action
    """
    def __init__(self, effect_primitive):
        self.target = CardTarget.from_primitive(effect_primitive.target)
        self.action = CardAction.from_primitive(effect_primitive.action)
        self.value = effect_primitive.value
        return


class CardTarget(Enum):
    """The receiver of a card's effect
    """
    OPPONENT = 0
    OWNER = 1

    @classmethod
    def from_primitive(cls, primitive):
        return next(t for t in cls if t.name == primitive.name)


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

    @classmethod
    def from_primitive(cls, primitive):
        return next(a for a in cls if a.name == primitive.name)


