import pytest
from realms.cardrepo import CardRepo, FactionPrimitive, ActionPrimitive, TargetPrimitive
from realms.card import CardFaction, CardTarget, CardAction
from pony.orm import db_session, select


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
