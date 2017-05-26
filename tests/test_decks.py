import pytest
from pytest import fixture
from realms.decks import MainDeck, PlayerDeck
from realms.exceptions import (
    MainDeckEmpty,
    PlayerDeckEmpty,
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


def test_playerdeck_discard(playerdeck):
    card = playerdeck._undrawn.pop()
    playerdeck.discard(card)
    assert card not in playerdeck._undrawn
    assert card in playerdeck._discards


def test_playerdeck_next_card_removed_from_undrawn(playerdeck):
    card = playerdeck._next_card()
    assert card not in playerdeck._undrawn


def test_playerdeck_next_card_raises_when_empty(playerdeck):
    for _ in range(10):
        playerdeck._next_card()  # empty out the deck
    with pytest.raises(PlayerDeckEmpty):
        playerdeck._next_card()


@given(n=strats.integers(min_value=1, max_value=10))
def test_playerdeck_next_card_triggers_refill(playerdeck, n):
    for _ in range(n):
        playerdeck.discard(playerdeck._undrawn.pop())
    popped = list()
    for _ in range(10 - n + 1):
        popped.append(playerdeck._next_card())
    assert len(playerdeck._undrawn) == (n - 1)
    # hypothesis doesn't generate a new playerdeck for each example
    # it generates, so you have to reconstruct the deck at the end
    playerdeck._undrawn += popped


@given(n=strats.integers(min_value=1))
def test_playerdeck_draw_one_at_a_time(playerdeck, n):
    cards = []
    for _ in range(n):
        try:
            cards += playerdeck.draw(num=1)
        except IndexError:
            break
    if n > 10:
        assert len(cards) == 10
    else:
        assert len(cards) == n
    playerdeck._undrawn += cards


@given(n=strats.integers(min_value=1))
def test_playerdeck_draw_multiple(playerdeck, n):
    cards = playerdeck.draw(n)
    if n > 10:
        assert len(cards) == 10
    else:
        assert len(cards) == n
    playerdeck._undrawn += cards


@given(n=strats.one_of(strats.integers(max_value=0),
                       strats.floats()))
def test_playerdeck_draw_bad_values(playerdeck, n):
    with pytest.raises(IndexError):
        playerdeck.draw(n)
