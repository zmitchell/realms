# -*- coding: utf-8 -*-
"""
.. module:: cardrepo
    :synopsis: Abstracts away the card loading mechanisms
.. moduleauthor:: Zach Mitchell <zmitchell@fastmail.com>
"""

from pony.orm import (
    Database,
    Required,
    Set,
    PrimaryKey,
    select,
    commit,
    db_session
)
from .cards import CardFaction, CardAction, CardTarget, Card
import json
from pkg_resources import resource_string, resource_exists
from uuid import uuid4

db = Database()


class CardRepo(object):
    """Provides an interface for the card-loading mechanisms
    """
    def __init__(self):
        self.db = db
        if not resource_exists(__package__, 'realms-cards.sqlite'):
            db.bind('sqlite', 'realms-cards.sqlite', create_db=True)
            db.generate_mapping(create_tables=True)
            _populate_db()
        else:
            db.bind('sqlite', 'realms-cards.sqlite')
            db.generate_mapping()

    @db_session
    def new_viper(self):
        """Produces a new instance of a Viper card

        Returns
        -------
        Card
            A new Viper
        """
        viper = self._named_card('Viper')
        return viper

    @db_session
    def new_scout(self):
        """Produces a new instance of a Scout card

        Returns
        -------
        Card
            A new Scout
        """
        scout = self._named_card('Scout')
        return scout

    @db_session
    def new_explorer(self):
        """Produces a new instance of an Explorer card

        Returns
        -------
        Card
            A new Explorer
        """
        explorer = self._named_card('Explorer')
        return explorer

    @db_session
    def _named_card(self, cardname):
        """Produces a new instance of a card with the given name

        Parameters
        ----------
        cardname : str
            The name of the card to produce

        Returns
        -------
        Card
            The card that was requested
        """
        primitive = select(c for c in CardPrimitive if c.name == cardname).first()
        new_uuid = uuid4()
        card = Card(primitive, new_uuid)
        return card

    @db_session
    def main_deck_cards(self):
        """Produces the list of cards suitable for the main deck

        The list of main deck cards does not contain Vipers, Scouts, or
        Explorers, but the ``MainDeck`` class does allow players to buy
        new Explorer cards.

        Returns
        -------
        [Card]
            A list of cards for the main deck

        Note
        ----
        The list of cards is not shuffled
        """
        primitives = select(c for c in CardPrimitive if c.count != 0)
        cards = []
        for p in primitives:
            for i in range(p.count):
                new_uuid = uuid4()
                card = Card(p, new_uuid)
                cards.append(card)
        return cards

    @db_session
    def player_deck_cards(self):
        """Produces the list of cards for a single player's starting deck

        Returns
        -------
        [Card]
            The list of cards for a player's starting deck

        Note
        ----
        The list of cards is not shuffled
        """
        scout_primitive = select(c for c in CardPrimitive if c.name == 'Scout').first()
        viper_primitive = select(c for c in CardPrimitive if c.name == 'Viper').first()
        cards = []
        for i in range(8):
            new_uuid = uuid4()
            scout = Card(scout_primitive, new_uuid)
            cards.append(scout)
        for i in range(2):
            new_uuid = uuid4()
            viper = Card(viper_primitive, new_uuid)
            cards.append(viper)
        return cards


class FactionPrimitive(db.Entity):
    """The ORM entity representing a ``CardFaction`` member
    """
    id = PrimaryKey(int, auto=True)
    """(int) Numeric identifier for the faction"""

    name = Required(str, unique=True)
    """(str) The display-style string for the faction"""

    cards = Set('CardPrimitive')
    """The set of ``CardPrimitive`` entities belonging to this faction"""


class TargetPrimitive(db.Entity):
    """The ORM entity representing a ``CardTarget`` member
    """
    id = PrimaryKey(int, auto=True)
    """(int) Numeric identifier for the target"""

    name = Required(str, unique=True)
    """(str) The display-style string for the target"""

    effects = Set('EffectPrimitive')
    """The set of ``EffectPrimitive`` entities with this target"""


class ActionPrimitive(db.Entity):
    """The ORM entity representing a ``CardAction`` member
    """
    id = PrimaryKey(int, auto=True)
    """(int) Numeric identifier for the action"""

    name = Required(str)
    """(str) The display-style string for the action"""

    effects = Set('EffectPrimitive')
    """The set of ``EffectPrimitive`` entities with this action"""


class EffectPrimitive(db.Entity):
    """The ORM entity representing a ``CardEffect``
    """
    id = PrimaryKey(int, auto=True)
    """(int) Numeric identifier for the effect (not used)"""

    target = Required(TargetPrimitive)
    """The target of the effect"""

    action = Required(ActionPrimitive)
    """The action to apply to the target"""

    value = Required(int, size=8)
    """The value of the action (how many cards to draw, money provided, etc.)"""

    cards = Set('CardPrimitive', reverse='effects')
    """The set of cards providing this effect (not used)"""

    allies = Set('CardPrimitive', reverse='ally')
    """The set of cards that provide this effect as an ally ability (not used)"""

    scraps = Set('CardPrimitive', reverse='scrap')
    """The set of cards that provide this effect when scrapped (not used)"""


class CardPrimitive(db.Entity):
    """The ORM entity representing a ``Card``
    """
    id = PrimaryKey(int, auto=True)
    """(int) Numeric identifier of the card"""

    name = Required(str)
    """(str) The name of the card"""

    faction = Required(FactionPrimitive)
    """(FactionPrimitive) The card's faction"""

    simplified = Required(bool)
    """(bool) Denotes whether the card's effects have been simplified to ease implementation"""

    base = Required(bool)
    """(bool) Denotes whether the card is a base"""

    outpost = Required(bool)
    """(bool) If the card is a base, denotes whether it is also an outpost"""

    defense = Required(int, size=8)
    """(int) If the card is a base, denotes the damage required to destroy it"""

    cost = Required(int, size=8)
    """(int) The amount of trade required to acquire the card"""

    effects = Set(EffectPrimitive, reverse='cards')
    """A list of effects provided by the card"""

    ally = Set(EffectPrimitive, reverse='allies')
    """A list of effects activated when another card of the same faction is played"""

    scrap = Set(EffectPrimitive, reverse='scraps')
    """A list of effects activated when the card is scrapped"""

    count = Required(int, size=8)
    """(int) The number of copies of this card present in the main deck
    (0 if unlimited or provided in each player's starting deck)"""


@db_session
def _populate_factions():
    """Populates the entries in the FactionPrimitives table

    Returns
    -------
    [FactionPrimitive]
        The list of FactionPrimitive entities created
    """
    factions = [FactionPrimitive(name=f.value) for f in CardFaction]
    commit()
    return factions


@db_session
def _populate_actions():
    """Populates the entries in the ActionPrimitives table

    Returns
    -------
    [ActionPrimitive]
        The list of ActionPrimitive entities created
    """
    actions = [ActionPrimitive(name=a.name) for a in CardAction]
    commit()
    return actions


@db_session
def _populate_targets():
    """Populates the entries in the TargetPrimitives table

    Returns
    -------
    [TargetPrimitive]
        The list of TargetPrimitives created
    """
    targets = [TargetPrimitive(name=t.name) for t in CardTarget]
    commit()
    return targets


def _populate_enums():
    action_entities = _populate_actions()
    faction_entities = _populate_factions()
    target_entities = _populate_targets()
    return action_entities, faction_entities, target_entities


@db_session
def _populate_db():
    """Populates the tables in ``realms-cards.sqlite`` from the data in ``cards.json``
    """
    json_string = resource_string('realms.resources', 'cards.json')
    json_cards = json.loads(json_string)
    actions, factions, targets = _populate_enums()
    for j in json_cards:
        _populate_card(j, actions, factions, targets)
        commit()
    return


@db_session
def _populate_card(card, actions, factions, targets):
    """Creates a single CardPrimitive entity from a JSON object

    Returns
    -------
    CardPrimitive
        The CardPrimitive entity that was created
    """
    card_faction = next(f for f in factions if f.name == card['faction'])
    card_effects = _populate_effects(card['effects'], targets, actions)
    card_ally_effects = _populate_effects(card['ally'], targets, actions)
    card_scrap_effects = _populate_effects(card['scrap'], targets, actions)
    populated_card = CardPrimitive(name=card['name'],
                                   faction=card_faction,
                                   simplified=_str_to_bool(card['simplified']),
                                   base=_str_to_bool(card['base']),
                                   outpost=_str_to_bool(card['outpost']),
                                   defense=int(card['defense']),
                                   cost=int(card['cost']),
                                   count=int(card['count']),
                                   effects=card_effects,
                                   ally=card_ally_effects,
                                   scrap=card_scrap_effects)
    return populated_card


@db_session
def _populate_effects(effect_list, targets, actions):
    """Creates a list of EffectsPrimitive entities from a list of JSON objects

    Returns
    -------
    [EffectPrimitive]
        The list of effects created from the list of JSON objects
    """
    effects = []
    for effect in effect_list:
        e_target = next(t for t in targets if t.name == effect['target'].upper())
        e_action = next(a for a in actions if a.name == effect['action'].upper())
        populated_effect = EffectPrimitive(target=e_target,
                                           action=e_action,
                                           value=int(effect['value']))
        effects.append(populated_effect)
    return effects


def _str_to_bool(string):
    """Converts "true" to ``True`` and "false" to ``False``
    """
    return True if string == 'true' else False



