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


def test_pitch_class_in_mode_degrees():
    assert 1 == PC.A.in_mode_degrees(base_pc=PC.A)
    assert 3 == PC.C.in_mode_degrees(base_pc=PC.A)
    assert "flat-2" == PC.B_FLAT.in_mode_degrees(base_pc=PC.A)
    assert 4 == PC.G.in_mode_degrees(base_pc=PC.D)
    assert 5 == PC.F.in_mode_degrees(base_pc=PC.B_FLAT)
    assert "#1" == PC.B.in_mode_degrees(base_pc=PC.B_FLAT)
