from pytest import fixture
from realms.decks import MainDeck


@fixture
def maindeck(repo):
    return MainDeck(repo)


def test_maindeck_shuffle_order(maindeck, repo):
    unshuffled = repo.main_deck_cards()
    shuffled = maindeck._cards
    assert unshuffled != shuffled


def test_maindeck_returns_none_when_empty(maindeck):
    num_cards = len(maindeck._cards)
    for i in range(num_cards):
        _ = maindeck.next_card()
    one_more = maindeck.next_card()
    assert one_more is None
