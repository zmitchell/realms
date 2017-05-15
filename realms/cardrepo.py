# -*- coding: utf-8 -*-
"""
.. module:: cardrepo
    :synopsis: Abstracts away the card loading mechanisms
.. moduleauthor:: Zach Mitchell <zmitchell@fastmail.com>
"""

from pony.orm import *
from realms.card import CardFaction, CardAction, CardTarget
import os
import json


db = Database()


class FactionPrimitive(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    cards = Set('CardPrimitive')


class TargetPrimitive(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    effects = Set('EffectPrimitive')


class ActionPrimitive(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    effects = Set('EffectPrimitive')


class EffectPrimitive(db.Entity):
    id = PrimaryKey(int, auto=True)
    target = Required(TargetPrimitive)
    action = Required(ActionPrimitive)
    value = Required(int, size=8)
    cards = Set('CardPrimitive', reverse='effects')
    allies = Set('CardPrimitive', reverse='ally')
    scraps = Set('CardPrimitive', reverse='scrap')


class CardPrimitive(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    faction = Required(FactionPrimitive)
    simplified = Required(bool)
    base = Required(bool)
    outpost = Required(bool)
    defense = Required(int, size=8)
    cost = Required(int, size=8)
    effects = Set(EffectPrimitive, reverse='cards')
    ally = Set(EffectPrimitive, reverse='allies')
    scrap = Set(EffectPrimitive, reverse='scraps')
    count = Required(int, size=8)


@db_session
def _populate_factions():
    """
    Adds the records to the Faction table

    :return: A list of Faction entities
    """
    factions = [FactionPrimitive(name=f.value) for f in CardFaction]
    commit()
    return factions


@db_session
def _populate_actions():
    """
    Adds the records to the Action table
    
    :return: A list of Action entities
    """
    actions = [ActionPrimitive(name=a.name) for a in CardAction]
    commit()
    return actions


@db_session
def _populate_targets():
    """
    Adds the records to the Target table
    
    :return: A list of Target entities
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
    with open('cards.json', 'r') as json_file:
        json_string = json_file.read()
        json_cards = json.loads(json_string)
    actions, factions, targets = _populate_enums()
    for j in json_cards:
        _ = _populate_card(j, actions, factions, targets)
        commit()
    return


@db_session
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


@db_session
def _populate_effects(effect_list, targets, actions):
    effects = []
    for effect in effect_list:
        e_target = next(t for t in targets if t.name == effect['target'])
        e_action = next(a for a in actions if a.name == effect['action'])
        populated_effect = EffectPrimitive(target=e_target,
                                           action=e_action,
                                           value=int(effect['value']))
        effects.append(populated_effect)
    return effects


def _str_to_bool(string):
    return True if string == 'true' else False


if not os.path.isfile('realms-cards.sqlite'):
    db.bind('sqlite', 'realms-cards.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
    _populate_db()
else:
    db.bind('sqlite', 'realms-cards.sqlite')
    db.generate_mapping()
