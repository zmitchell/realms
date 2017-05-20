from realms.card import CardFaction
from realms.cardrepo import FactionPrimitive
from pony.orm import select, db_session
import pytest


@pytest.fixture
@db_session
def primitive():
    return select(f for f in FactionPrimitive).first()


def test_faction_str_representation():
    fac = CardFaction.star
    assert str(fac) == 'Star Empire'


@db_session
def test_faction_from_primitive(primitive):
    faction = CardFaction.from_primitive(primitive)
    assert faction.name == primitive.name
