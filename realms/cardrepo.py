# -*- coding: utf-8 -*-
"""
.. module:: cardrepo
    :synopsis: Abstracts away the card loading mechanisms
.. moduleauthor:: Zach Mitchell <zmitchell@fastmail.com>
"""


class CardRepo(object):
    """
    Provides an interface for card storage
    """
    def __init__(self, db):
        pass

    def load_cards(self):
        """
        Returns the entire list of cards from storage
        """
        pass
