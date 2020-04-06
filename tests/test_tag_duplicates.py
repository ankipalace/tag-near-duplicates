from util import read_notes, pre_process


import pytest


@pytest.fixture
def notes():
    return read_notes("data/step1-slice.txt")


def test_read_notes(notes):
    assert not notes.empty


def test_pre_process(notes):
    notes = pre_process(notes)

    assert notes.loc[-37938811912]["set"] == (
        "a2 anti effects glucocorticoids inducing inflammatory "
        "inhibitor lipocortin may phospholipase synthesis"
    )

    assert notes.loc[-37938811912]["clean"] == (
        "glucocorticoids may have anti inflammatory effects by inducing "
        "the synthesis of  lipocortin   an inhibitor of  phospholipase a2  "
    )

    assert notes.loc[-37938811912]["text"] == (
        "Glucocorticoids may have anti-inflammatory effects by inducing the synthesis of {{c1::lipocortin}}, "
        "an inhibitor of {{c2::phospholipase A2}} "
    )
