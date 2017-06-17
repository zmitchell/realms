from pytest import fixture, raises
from realms.decks import (
    MainDeck,
    PlayerDeck,
    Hand
)
from realms.cards import CardFaction, CardAction
from realms.exceptions import (
    HandInitError
)
from hypothesis import given, assume
import hypothesis.strategies as strats
from collections import Counter


MAX_CARD_INDEX = 200


@fixture
def maindeck(repo):
    return MainDeck(repo)


@fixture
def maindeck_cards(repo):
    cards = repo.main_deck_cards()
    return cards


@fixture
def blob_cards(maindeck_cards):
    return [c for c in maindeck_cards if c.faction == CardFaction.BLOB]


@fixture
def federation_cards(maindeck_cards):
    return [c for c in maindeck_cards if c.faction == CardFaction.FEDERATION]


@fixture
def star_cards(maindeck_cards):
    return [c for c in maindeck_cards if c.faction == CardFaction.STAR]


@fixture
def machine_cards(maindeck_cards):
    return [c for c in maindeck_cards if c.faction == CardFaction.MACHINE]


@fixture
def mech_world(maindeck_cards):
    return next(c for c in maindeck_cards if c.name == 'Mech World')


@fixture
def playerdeck(repo):
    return PlayerDeck(repo.player_deck_cards())


@fixture
def basic_hand(playerdeck):
    return Hand(5, [], playerdeck)


@fixture
def blob_hand(playerdeck, blob_cards):
    playerdeck._undrawn += blob_cards
    return Hand(5, [], playerdeck)


def test_hand_empty_deck(playerdeck):
    playerdeck.undrawn = []
    hand = Hand(5, [], playerdeck)
    assert hand is not None


@given(n=strats.integers())
def test_hand_draw_number(playerdeck, n):
    assume((n < 0) or (n > 5))
    with raises(HandInitError):
        Hand(n, [], playerdeck)


def test_hand_basic_effects_uuids(basic_hand):
    basic_effects = Hand._collect_basic_effects(basic_hand.cards)
    card_uuids = [c.uuid for c in basic_hand.cards]
    effect_uuids = [e.uuid for c in basic_hand.cards for e in c.effects_basic]
    for e in basic_effects:
        assert e.provider in card_uuids
        assert e.uuid in effect_uuids


def test_hand_ally_factions_no_allies(basic_hand):
    ally_factions = Hand._collect_ally_factions(basic_hand.cards)
    assert len(ally_factions) == 0


def test_hand_ally_factions_one_faction(basic_hand, blob_cards):
    basic_hand.cards = blob_cards
    ally_factions = Hand._collect_ally_factions(basic_hand.cards)
    assert len(ally_factions) == 1
    assert ally_factions[0] == CardFaction.BLOB


def test_hand_ally_factions_every_faction(basic_hand, blob_cards, star_cards,
                                          federation_cards, machine_cards):
    cards = blob_cards + star_cards + federation_cards + machine_cards
    basic_hand.cards = cards
    ally_factions = Hand._collect_ally_factions(basic_hand.cards)
    assert len(set(ally_factions)) == 4


@given(ids=strats.tuples(strats.integers(min_value=0, max_value=MAX_CARD_INDEX),
                         strats.integers(min_value=0, max_value=MAX_CARD_INDEX),
                         strats.integers(min_value=0, max_value=MAX_CARD_INDEX),
                         strats.integers(min_value=0, max_value=MAX_CARD_INDEX),
                         strats.integers(min_value=0, max_value=MAX_CARD_INDEX)))
def test_hand_ally_factions_mixed_hand(basic_hand, maindeck_cards, ids):
    for i in ids:
        assume(i < len(maindeck_cards))
    cards = [maindeck_cards[i] for i in ids]
    basic_hand.cards = cards
    counts = Counter([c.faction for c in basic_hand.cards])
    ally_factions = Hand._collect_ally_factions(basic_hand.cards)
    for fac in counts.keys():
        if (fac == CardFaction.UNALIGNED) or (fac == CardFaction.ALL):
            continue
        if counts[fac] > 1:
            assert fac in ally_factions


def test_hand_ally_factions_mech_world(basic_hand, mech_world):
    basic_hand.cards.append(mech_world)
    ally_factions = Hand._collect_ally_factions(basic_hand.cards)
    assert len(set(ally_factions)) == 4


def test_hand_ally_effects_uuids(basic_hand, blob_cards):
    ally_cards =  blob_cards[:2]
    basic_hand.cards += ally_cards
    faction = [CardFaction.BLOB]
    ally_effects = Hand._collect_ally_effects(basic_hand.cards, faction)
    ally_uuids = [c.uuid for c in ally_cards]
    effect_uuids = [e.uuid for c in ally_cards for e in c.effects_ally]
    for e in ally_effects:
        assert e.provider in ally_uuids
        assert e.uuid in effect_uuids


@given(ids=strats.tuples(strats.integers(min_value=0, max_value=MAX_CARD_INDEX),
                         strats.integers(min_value=0, max_value=MAX_CARD_INDEX),
                         strats.integers(min_value=0, max_value=MAX_CARD_INDEX),
                         strats.integers(min_value=0, max_value=MAX_CARD_INDEX),
                         strats.integers(min_value=0, max_value=MAX_CARD_INDEX)))
def test_hand_collect_effects_uuids(basic_hand, maindeck_cards, ids):
    for i in ids:
        assume(i < len(maindeck_cards))
    cards = [maindeck_cards[i] for i in ids]
    basic_hand.cards = cards
    card_uuids = [c.uuid for c in basic_hand.cards]
    effects = basic_hand._collect_effects()
    for e in effects:
        assert e.provider in card_uuids

