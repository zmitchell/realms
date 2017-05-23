from realms.card import CardFaction, CardTarget, CardAction
from realms.cardrepo import FactionPrimitive, TargetPrimitive, ActionPrimitive, CardRepo
from pony.orm import select, db_session
import pytest


@pytest.fixture(scope='module')
def repo():
    repo = CardRepo()
    return repo


@pytest.fixture
@db_session
def faction_primitives(repo):
    return select(f for f in FactionPrimitive)[:]


def test_faction_str_representation():
    fac = CardFaction.STAR
    assert str(fac) == 'Star Empire'


def test_faction_from_primitive(faction_primitives):
    for primitive in faction_primitives:
        faction = CardFaction.from_primitive(primitive)
        assert faction.value == primitive.name


@pytest.fixture
@db_session
def target_primitives(repo):
    return select(t for t in TargetPrimitive)[:]


def test_target_from_primitive(target_primitives):
    for primitive in target_primitives:
        target = CardTarget.from_primitive(primitive)
        assert target.name == primitive.name


@pytest.fixture
@db_session
def action_primitives(repo):
    return select(a for a in ActionPrimitive)[:]


def test_action_from_primitive(action_primitives):
    for primitive in action_primitives:
        action = CardAction.from_primitive(primitive)
        assert action.name == primitive.name


@db_session
def test_cardrepo_produce_new_viper(repo):
    viper = repo.new_viper()
    v_effect = viper.effects_basic[0]
    assert viper.faction == CardFaction.UNALIGNED
    assert viper.cost == 0
    assert viper.base == False


@db_session
def test_cardrepo_viper_effects(repo):
    viper = repo.new_viper()
    v_effect = viper.effects_basic[0]
    assert v_effect.target == CardTarget.OPPONENT
    assert v_effect.action == CardAction.ATTACK
    assert v_effect.value == 1


@db_session
def test_cardrepo_produce_new_scout(repo):
    scout = repo.new_scout()
    assert scout.faction == CardFaction.UNALIGNED
    assert scout.cost == 0
    assert scout.base == False


@db_session
def test_cardrepo_scout_effects(repo):
    scout = repo.new_scout()
    s_effect = scout.effects_basic[0]
    assert s_effect.target == CardTarget.OWNER
    assert s_effect.action == CardAction.MONEY
    assert s_effect.value == 1

