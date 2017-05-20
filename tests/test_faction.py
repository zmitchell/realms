from realms.card import CardFaction
from realms.cardrepo import FactionPrimitive
from pony.orm import select, db_session
import pytest


@pytest.fixture
@db_session
def primitives():
    return select(f for f in FactionPrimitive)


def test_faction_str_representation():
    fac = CardFaction.STAR
    assert str(fac) == 'Star Empire'


@db_session
def test_faction_from_primitive(primitives):
    for primitive in primitives:
        faction = CardFaction.from_primitive(primitive)
        assert faction.value == primitive.name
