# -*- coding: utf-8 -*-
"""
.. module:: player
    :synopsis: Provides the Player class
.. moduleauthor:: Zach Mitchell <zmitchell@fastmail.com>
"""


from .deck import PlayerDeck


class Player(object):
    """
    Represents a single player
    """
    def __init__(self, name):
        self.name = name
        self._deck = PlayerDeck()
        self._cards_drawn = self._deck.draw()  # draws 5 by default
        self._bases = None
        self._queued_effects = None
        self._health = 50
        self._money = 0
        pass


