from realms.card import CardFaction, CardTarget, CardAction
from realms.cardrepo import CardRepo
from pony.orm import db_session
import pytest


@pytest.fixture(scope='module')
def repo():
    repo = CardRepo()
    return repo


@pytest.fixture
def viper(repo):
    return repo.new_viper()


def test_viper_properties(viper):
    assert viper.faction == CardFaction.UNALIGNED
    assert viper.cost == 0
    assert viper.base is False


def test_viper_effects_basic(viper):
    v_effect = viper.effects_basic[0]
    assert v_effect.target == CardTarget.OPPONENT
    assert v_effect.action == CardAction.ATTACK
    assert v_effect.value == 1


def test_viper_effects_number(viper):
    assert len(viper.effects_basic) == 1
    assert len(viper.effects_ally) == 0
    assert len(viper.effects_scrap) == 0


@pytest.fixture
def scout(repo):
    return repo.new_scout()


def test_scout_properties(scout):
    assert scout.faction == CardFaction.UNALIGNED
    assert scout.cost == 0
    assert scout.base is False


def test_scout_effects_basic(scout):
    s_effect = scout.effects_basic[0]
    assert s_effect.target == CardTarget.OWNER
    assert s_effect.action == CardAction.MONEY
    assert s_effect.value == 1


def test_scout_effects_number(scout):
    assert len(scout.effects_basic) == 1
    assert len(scout.effects_ally) == 0
    assert len(scout.effects_scrap) == 0


@pytest.fixture
def explorer(repo):
    return repo.new_explorer()


def test_explorer_properties(explorer):
    assert explorer.faction == CardFaction.UNALIGNED
    assert explorer.cost == 0
    assert explorer.base is False


def test_explorer_effects_basic(explorer):
    effect = explorer.effects_basic[0]
    assert effect.target == CardTarget.OWNER
    assert effect.action == CardAction.MONEY
    assert effect.value == 2


def test_explorer_effects_scrap(explorer):
    effect = explorer.effects_scrap[0]
    assert effect.target == CardTarget.OPPONENT
    assert effect.action == CardAction.ATTACK
    assert effect.value == 2


def test_explorer_effects_number(explorer):
    assert len(explorer.effects_basic) == 1
    assert len(explorer.effects_ally) == 0
    assert len(explorer.effects_scrap) == 1


@pytest.fixture
def main_deck_cards(repo):
    return repo.main_deck_cards()


def test_main_deck_length(main_deck_cards):
    assert len(main_deck_cards) > 0


def test_main_deck_cards_does_not_contain_vipers(main_deck_cards):
    with pytest.raises(StopIteration):
        next(c for c in main_deck_cards if c.name == 'Viper')


def test_main_deck_cards_does_not_contain_scouts(main_deck_cards):
    with pytest.raises(StopIteration):
        next(c for c in main_deck_cards if c.name == 'Scout')


def test_main_deck_cards_does_not_contain_explorers(main_deck_cards):
    with pytest.raises(StopIteration):
        next(c for c in main_deck_cards if c.name == 'Explorer')
