import pytest
from pytest import fixture
from realms.decks import MainDeck, PlayerDeck
from realms.exceptions import (
    MainDeckEmpty,
    PlayerDeckInitSize,
    PlayerDeckInitContents
)
from hypothesis import given, assume
import hypothesis.strategies as strats


@fixture
def maindeck(repo):
    return MainDeck(repo)


@fixture
def maindeck_cards(repo):
    cards = repo.main_deck_cards()
    return cards


def test_maindeck_shuffle_order(maindeck, repo):
    unshuffled = repo.main_deck_cards()
    shuffled = maindeck._cards
    assert unshuffled != shuffled


def test_maindeck_raises_exception_when_empty(maindeck):
    num_cards = len(maindeck._cards)
    for i in range(num_cards):
        maindeck.next_card()
    with pytest.raises(MainDeckEmpty):
        maindeck.next_card()


@given(n=strats.integers(min_value=-10, max_value=10))
def test_playerdeck_init_size(repo, n):
    assume(n != 0)
    cards = []
    for i in range(PlayerDeck.starting_size + n):
        cards.append(repo.new_viper())
    with pytest.raises(PlayerDeckInitSize):
        PlayerDeck(cards)


def test_playerdeck_init_contents(repo):
    vipers = [repo.new_viper() for _ in range(2)]
    scouts = [repo.new_scout() for _ in range(7)]
    others = [repo._named_card('Cutter')]
    cards = vipers + scouts + others
    with pytest.raises(PlayerDeckInitContents):
        PlayerDeck(cards)


@fixture
def playerdeck(repo):
    return PlayerDeck(repo.player_deck_cards())


def test_playerdeck_undrawn_refilled(playerdeck):
    playerdeck._discards = playerdeck._undrawn
    playerdeck._undrawn = []
    playerdeck._refill_undrawn()
    assert len(playerdeck._undrawn) == 10
    assert len(playerdeck._discards) == 0
