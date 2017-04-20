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

    :param uuid_: unique identifier for the card
    :param name_: display name of the card
    :type name_: string
    :param is_base_: is the card a base
    :type is_base_: bool
    :param is_outpost_: if the card is a base, is it an outpost
    :type is_outpost_: bool
    :param health: if the card is a base, the damage it can take
    :type health: int
    :param cost_: cost to buy the card
    :type cost_: int
    :param faction_: faction to which the card belongs
    :type faction_: Faction
    :param effects_: effect(s) provided by the card
    :type effects_: list of Effect objects
    :param ally_ability_: effect provided when at least one other card
                          of the same faction is played
    :type ally_ability_: Effect
    :param image_: display image for the card

    .. note:: The UUID format has not been determined yet.
    .. note:: The image format has not been determined yet.
    """

    def __init__(self, uuid_, name_, is_base_=False, is_outpost_=False, health_=None,
                 cost_=None, faction_=None, effects_=None, ally_ability_=None, image_=None):
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


class Effect(object):
    """
    A single effect provided by a card
    """
    pass


class Target(Enum):
    """
    The receiver of an effect from a card
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

