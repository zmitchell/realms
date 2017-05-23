# -*- coding: utf-8 -*-
"""
.. module:: cardrepo
    :synopsis: Abstracts away the card loading mechanisms
.. moduleauthor:: Zach Mitchell <zmitchell@fastmail.com>
"""

import pony.orm as pny
from .card import CardFaction, CardAction, CardTarget, Card
import json
from pkg_resources import resource_string, resource_exists
from uuid import uuid4

db = pny.Database()


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

    @pny.db_session
    def new_viper(self):
        viper = self._named_card('Viper')
        return viper

    @pny.db_session
    def new_scout(self):
        scout = self._named_card('Scout')
        return scout

    @pny.db_session
    def _named_card(self, cardname):
        primitive = pny.select(c for c in CardPrimitive if c.name == cardname).first()
        new_uuid = uuid4()
        card = Card(primitive, new_uuid)
        return card


class FactionPrimitive(db.Entity):
    """The ORM entity representing a ``CardFaction`` member
    """
    id = pny.PrimaryKey(int, auto=True)
    """(int) Numeric identifier for the faction"""

    name = pny.Required(str, unique=True)
    """(str) The display-style string for the faction"""

    cards = pny.Set('CardPrimitive')
    """The set of ``CardPrimitive`` entities belonging to this faction"""


class TargetPrimitive(db.Entity):
    """The ORM entity representing a ``CardTarget`` member
    """
    id = pny.PrimaryKey(int, auto=True)
    """(int) Numeric identifier for the target"""

    name = pny.Required(str, unique=True)
    """(str) The display-style string for the target"""

    effects = pny.Set('EffectPrimitive')
    """The set of ``EffectPrimitive`` entities with this target"""


class ActionPrimitive(db.Entity):
    """The ORM entity representing a ``CardAction`` member
    """
    id = pny.PrimaryKey(int, auto=True)
    """(int) Numeric identifier for the action"""

    name = pny.Required(str)
    """(str) The display-style string for the action"""

    effects = pny.Set('EffectPrimitive')
    """The set of ``EffectPrimitive`` entities with this action"""


class EffectPrimitive(db.Entity):
    """The ORM entity representing a ``CardEffect``
    """
    id = pny.PrimaryKey(int, auto=True)
    """(int) Numeric identifier for the effect (not used)"""

    target = pny.Required(TargetPrimitive)
    """The target of the effect"""

    action = pny.Required(ActionPrimitive)
    """The action to apply to the target"""

    value = pny.Required(int, size=8)
    """The value of the action (how many cards to draw, money provided, etc.)"""

    cards = pny.Set('CardPrimitive', reverse='effects')
    """The set of cards providing this effect (not used)"""

    allies = pny.Set('CardPrimitive', reverse='ally')
    """The set of cards that provide this effect as an ally ability (not used)"""

    scraps = pny.Set('CardPrimitive', reverse='scrap')
    """The set of cards that provide this effect when scrapped (not used)"""


class CardPrimitive(db.Entity):
    """The ORM entity representing a ``Card``
    """
    id = pny.PrimaryKey(int, auto=True)
    """(int) Numeric identifier of the card"""

    name = pny.Required(str)
    """(str) The name of the card"""

    faction = pny.Required(FactionPrimitive)
    """(FactionPrimitive) The card's faction"""

    simplified = pny.Required(bool)
    """(bool) Denotes whether the card's effects have been simplified to ease implementation"""

    base = pny.Required(bool)
    """(bool) Denotes whether the card is a base"""

    outpost = pny.Required(bool)
    """(bool) If the card is a base, denotes whether it is also an outpost"""

    defense = pny.Required(int, size=8)
    """(int) If the card is a base, denotes the damage required to destroy it"""

    cost = pny.Required(int, size=8)
    """(int) The amount of trade required to acquire the card"""

    effects = pny.Set(EffectPrimitive, reverse='cards')
    """A list of effects provided by the card"""

    ally = pny.Set(EffectPrimitive, reverse='allies')
    """A list of effects activated when another card of the same faction is played"""

    scrap = pny.Set(EffectPrimitive, reverse='scraps')
    """A list of effects activated when the card is scrapped"""

    count = pny.Required(int, size=8)
    """(int) The number of copies of this card present in the main deck
    (0 if unlimited or provided in each player's starting deck)"""


@pny.db_session
def _populate_factions():
    """Populates the entries in the FactionPrimitives table

    Returns
    -------
    [FactionPrimitive]
        The list of FactionPrimitive entities created
    """
    factions = [FactionPrimitive(name=f.value) for f in CardFaction]
    pny.commit()
    return factions


@pny.db_session
def _populate_actions():
    """Populates the entries in the ActionPrimitives table

    Returns
    -------
    [ActionPrimitive]
        The list of ActionPrimitive entities created
    """
    actions = [ActionPrimitive(name=a.name) for a in CardAction]
    pny.commit()
    return actions


@pny.db_session
def _populate_targets():
    """Populates the entries in the TargetPrimitives table

    Returns
    -------
    [TargetPrimitive]
        The list of TargetPrimitives created
    """
    targets = [TargetPrimitive(name=t.name) for t in CardTarget]
    pny.commit()
    return targets


def _populate_enums():
    action_entities = _populate_actions()
    faction_entities = _populate_factions()
    target_entities = _populate_targets()
    return action_entities, faction_entities, target_entities


@pny.db_session
def _populate_db():
    """Populates the tables in ``realms-cards.sqlite`` from the data in ``cards.json``
    """
    json_string = resource_string('realms.resources', 'cards.json')
    json_cards = json.loads(json_string)
    actions, factions, targets = _populate_enums()
    for j in json_cards:
        _populate_card(j, actions, factions, targets)
        pny.commit()
    return


@pny.db_session
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


@pny.db_session
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



