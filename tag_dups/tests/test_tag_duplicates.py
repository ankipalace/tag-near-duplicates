from tag_dups.util import read_notes, pre_process
from tag_dups.tag_duplicates import simple_dups, fuzzy_dups


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
        "the synthesis of lipocortin an inhibitor of phospholipase a2"
    )

    assert notes.loc[-37938811912]["text"] == (
        "Glucocorticoids may have anti-inflammatory effects by inducing the "
        "synthesis of {{c1::lipocortin}}, "
        "an inhibitor of {{c2::phospholipase A2}} "
    )


def test_simple_dups(notes):
    df = pre_process(notes)
    df = simple_dups(df)
    exp = [
        -37771074946,
        -17771074946,
        -17771305162,
        -27771305162,
        -37771305162,
        -37871982399,
        -37868125544,
    ]
    locs = df[df.duplicate.notnull()].index.tolist()
    assert sorted(locs) == sorted(exp)


def test_fuzzy_dups(notes):
    df1 = pre_process(notes)
    # simple_dups will be run first in practice
    # TODO: Test append=True
    df2 = read_notes("data/step2-slice.txt")
    df2 = pre_process(df2)
    # Insert item that should be caught by fuzzy string matching
    df2.loc["manual_dup", "clean"] = (
        "glucocorticoids could quite possibly have anti inflammatory "
        "effects by inducing the synthesis of lipocortin an inhibitor of "
        "phospholipase a2"
    )
    tagged = fuzzy_dups(df1, df2, append=False)
    assert not tagged.empty
    assert not tagged.duplicate.empty
