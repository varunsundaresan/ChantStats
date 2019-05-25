from music21.note import Note

from .context import chantstats
from chantstats.v2.pitch_class import PC


def test_pitch_class():
    assert "A" == PC.A == PC("A")
    assert "B-" == PC.B_FLAT == PC("B-")
    assert "C" == PC.C == PC("C")


def test_pitch_class_from_note():
    assert "A" == PC.A == PC.from_note(Note("A4"))
    assert "B-" == PC.B_FLAT == PC.from_note(Note("B-3"))
    assert "G" == PC.G == PC.from_note(Note("G2"))


def test_pitch_class_description():
    assert "A" == PC.A.descr
    assert "B-" == PC.B_FLAT.descr
    assert "F" == PC.F.descr
    assert "G" == PC.G.descr
