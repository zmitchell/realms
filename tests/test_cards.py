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


@pytest.fixture
@db_session
def viper(repo):
    return repo.new_viper()


def test_cardrepo_viper_properties(viper):
    assert viper.faction == CardFaction.UNALIGNED
    assert viper.cost == 0
    assert viper.base is False


def test_cardrepo_viper_effects_basic(viper):
    v_effect = viper.effects_basic[0]
    assert v_effect.target == CardTarget.OPPONENT
    assert v_effect.action == CardAction.ATTACK
    assert v_effect.value == 1


def test_cardrepo_viper_effects_number(viper):
    assert len(viper.effects_basic) == 1
    assert len(viper.effects_ally) == 0
    assert len(viper.effects_scrap) == 0


@pytest.fixture
@db_session
def scout(repo):
    return repo.new_scout()


def test_cardrepo_scout_properties(scout):
    assert scout.faction == CardFaction.UNALIGNED
    assert scout.cost == 0
    assert scout.base is False


def test_cardrepo_scout_effects_basic(scout):
    s_effect = scout.effects_basic[0]
    assert s_effect.target == CardTarget.OWNER
    assert s_effect.action == CardAction.MONEY
    assert s_effect.value == 1


def test_cardrepo_scout_effects_number(scout):
    assert len(scout.effects_basic) == 1
    assert len(scout.effects_ally) == 0
    assert len(scout.effects_scrap) == 0


@pytest.fixture
@db_session
def explorer(repo):
    return repo.new_explorer()


def test_cardrepo_explorer_properties(explorer):
    assert explorer.faction == CardFaction.UNALIGNED
    assert explorer.cost == 0
    assert explorer.base is False


def test_cardrepo_explorer_effects_basic(explorer):
    effect = explorer.effects_basic[0]
    assert effect.target == CardTarget.OWNER
    assert effect.action == CardAction.MONEY
    assert effect.value == 2


def test_cardrepo_explorer_effects_scrap(explorer):
    effect = explorer.effects_scrap[0]
    assert effect.target == CardTarget.OPPONENT
    assert effect.action == CardAction.ATTACK
    assert effect.value == 2


def test_cardrepo_explorer_effects_number(explorer):
    assert len(explorer.effects_basic) == 1
    assert len(explorer.effects_ally) == 0
    assert len(explorer.effects_scrap) == 1

