from pytest import fixture
from pytest import raises as ptraises
from realms.decks import MainDeck
from realms.exceptions import MainDeckEmpty


@fixture
def maindeck(repo):
    return MainDeck(repo)


def test_maindeck_shuffle_order(maindeck, repo):
    unshuffled = repo.main_deck_cards()
    shuffled = maindeck._cards
    assert unshuffled != shuffled


def test_maindeck_raises_exception_when_empty(maindeck):
    num_cards = len(maindeck._cards)
    for i in range(num_cards):
        maindeck.next_card()
    with ptraises(MainDeckEmpty):
        maindeck.next_card()