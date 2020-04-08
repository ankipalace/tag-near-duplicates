from util import read_notes, pre_process
from tag_duplicates import simple_dups


import pytest


@pytest.fixture
def notes():
    return read_notes("data/step1-slice.txt")


def test_read_notes(notes):
    assert not notes.empty


def test_pre_process(notes):

    assert notes.loc[-37938811912]["set"] == (
        "a2 anti effects glucocorticoids inducing inflammatory "
        "inhibitor lipocortin may phospholipase synthesis"
    )

    assert notes.loc[-37938811912]["clean"] == (
        "glucocorticoids may have anti inflammatory effects by inducing "
        "the synthesis of lipocortin an inhibitor of phospholipase a2"
    )

    assert notes.loc[-37938811912]["text"] == (
        "Glucocorticoids may have anti-inflammatory effects by inducing the synthesis of {{c1::lipocortin}}, "
        "an inhibitor of {{c2::phospholipase A2}} "
    )


def test_simple_dups(notes):
    df = simple_dups(notes)
    exp = [
        -37771074946, -17771074946,
        -17771305162, -27771305162,
        -37771305162,  -37871982399,
        -37868125544
    ]
    locs = df[df.dup.notnull()].index.tolist()
    assert sorted(locs) == sorted(exp)
