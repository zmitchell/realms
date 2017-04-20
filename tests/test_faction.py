from realms.card import Faction


def test_faction_str_representation():
    fac = Faction.star
    assert str(fac) == 'Star Empire'
