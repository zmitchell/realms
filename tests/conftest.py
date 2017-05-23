import pytest
from realms.cardrepo import CardRepo


@pytest.fixture(scope='session')
def repo():
    repo = CardRepo()
    return repo
