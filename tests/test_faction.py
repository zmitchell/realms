from realms.card import Faction
from realms.card import CardFaction


def test_faction_str_representation():
    fac = Faction.star
    fac = CardFaction.star
    assert str(fac) == 'Star Empire'
