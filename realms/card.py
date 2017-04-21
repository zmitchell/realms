# -*- coding: utf-8 -*-
"""
.. module:: card
    :synopsis: Encapsulate card behavior
.. moduleauthor:: Zach Mitchell <zmitchell@fastmail.com>
"""

from enum import Enum


class Card(object):
    """
    Card class

    This class encapsulates the behavior and data of a single card, be it
    a ship or base.

    :param uuid: unique identifier for the card
    :type uuid: UUID
    :param name: display name of the card
    :type name: string
    :param is_base: is the card a base
    :type is_base: bool
    :param is_outpost: if the card is a base, is it an outpost
    :type is_outpost: bool
    :param health: if the card is a base, the damage it can take
    :type health: int
    :param cost: cost to buy the card
    :type cost: int
    :param faction: faction to which the card belongs
    :type faction: Faction
    :param effects: effect(s) provided by the card
    :type effects: [CardEffect]
    :param ally_ability: effect provided when at least one other card
                          of the same faction is played
    :type ally_ability: CardEffect
    :param image: display image for the card

    .. note:: The UUID format has not been determined yet.
    .. note:: The image format has not been determined yet.
    """

    def __init__(self, uuid, name, is_base=False, is_outpost=False, health=None,
                 cost=None, faction=None, effects=None, ally_ability=None, image=None):
        pass


class Faction(Enum):
    """
    The set of allowed factions for cards.
    """
    unaligned = 'Unaligned'
    star = 'Star Empire'
    blob = 'Blob'
    federation = 'Federation'
    machine = 'Machine Cult'

    def __str__(self):
        """
        String representation of the object

        The value of an enumeration member is typically set to an integer
        that is never used, but here the value is set to the full display
        string of the faction so it can be used as the string representation
        of the faction.

        :return String representation of the faction
        :rtype str

        Example::

            >>> fac = Faction.star
            >>> str(fac)
            Star Empire
        """
        return self.value


class CardEffect(object):
    """
    A single effect provided by a card

    Identifies an action (attack, discard, etc), any values associated
    with the action (attack damage, number of cards to discard, etc),
    and whether the action should be applied to the owner of the card
    (healing, scrapping, etc) or to an opponent (attack, discard, etc).

    :param target: The player who should receive the effect of the card
    :type target: CardTarget
    :param action: The type of action to apply
    :type action: CardAction
    :param value: The value associated with the action
    :type value: int
    """
    def __init__(self, target, action, value):
        self.target = target
        self.action = action
        self.value = value
        return


class CardTarget(Enum):
    """
    The receiver of a card's effect
    """
    owner = 0
    opponent = 1


class CardAction(Enum):
    """
    The type of action that an effect entails
    """
    attack = 0
    heal = 1
    draw = 2
    scrap = 3
    acquire = 4
    discard = 5
    money = 6

