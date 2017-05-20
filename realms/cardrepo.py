# -*- coding: utf-8 -*-
"""
.. module:: cardrepo
    :synopsis: Abstracts away the card loading mechanisms
.. moduleauthor:: Zach Mitchell <zmitchell@fastmail.com>
"""

import pony.orm as pny
from .card import CardFaction, CardAction, CardTarget
import json
from pkg_resources import resource_string, resource_exists

db = pny.Database()


class FactionPrimitive(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    name = pny.Required(str, unique=True)
    cards = pny.Set('CardPrimitive')


class TargetPrimitive(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    name = pny.Required(str, unique=True)
    effects = pny.Set('EffectPrimitive')


class ActionPrimitive(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    name = pny.Required(str)
    effects = pny.Set('EffectPrimitive')


class EffectPrimitive(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    target = pny.Required(TargetPrimitive)
    action = pny.Required(ActionPrimitive)
    value = pny.Required(int, size=8)
    cards = pny.Set('CardPrimitive', reverse='effects')
    allies = pny.Set('CardPrimitive', reverse='ally')
    scraps = pny.Set('CardPrimitive', reverse='scrap')


class CardPrimitive(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    name = pny.Required(str)
    faction = pny.Required(FactionPrimitive)
    simplified = pny.Required(bool)
    base = pny.Required(bool)
    outpost = pny.Required(bool)
    defense = pny.Required(int, size=8)
    cost = pny.Required(int, size=8)
    effects = pny.Set(EffectPrimitive, reverse='cards')
    ally = pny.Set(EffectPrimitive, reverse='allies')
    scrap = pny.Set(EffectPrimitive, reverse='scraps')
    count = pny.Required(int, size=8)


@pny.db_session
def _populate_factions():
    """
    Adds the records to the Faction table

    :return: A list of Faction entities
    """
    factions = [FactionPrimitive(name=f.value) for f in CardFaction]
    pny.commit()
    return factions


@pny.db_session
def _populate_actions():
    """
    Adds the records to the Action table

    :return: A list of Action entities
    """
    actions = [ActionPrimitive(name=a.name) for a in CardAction]
    pny.commit()
    return actions


@pny.db_session
def _populate_targets():
    """
    Adds the records to the Target table

    :return: A list of Target entities
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
    json_string = resource_string('realms.resources', 'cards.json')
    json_cards = json.loads(json_string)
    actions, factions, targets = _populate_enums()
    for j in json_cards:
        _populate_card(j, actions, factions, targets)
        pny.commit()
    return


@pny.db_session
def _populate_card(card, actions, factions, targets):
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
    return True if string == 'true' else False


if not resource_exists(__package__, 'realms-cards.sqlite'):
    db.bind('sqlite', 'realms-cards.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
    _populate_db()
else:
    db.bind('sqlite', 'realms-cards.sqlite')
    db.generate_mapping()
