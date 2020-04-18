from tag_dups.util import read_notes

import pytest


@pytest.fixture
def notes():
    return read_notes("data/step1-slice.txt")
