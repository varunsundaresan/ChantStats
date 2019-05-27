from music21.note import Note

from .context import chantstats
from chantstats.v2.mode_degree import ModeDegree
from chantstats.v2.pitch_class import PC


def test_mode_degrees_from_note_pairs():
    assert 1 == ModeDegree.from_note_pair(note=Note("D3"), base_note=Note("D3"))
    assert 1 == ModeDegree.from_note_pair(note=Note("E3"), base_note=Note("E3"))
    assert 1 == ModeDegree.from_note_pair(note=Note("F3"), base_note=Note("F3"))
    assert 1 == ModeDegree.from_note_pair(note=Note("G3"), base_note=Note("G3"))
    assert 1 == ModeDegree.from_note_pair(note=Note("A3"), base_note=Note("A3"))
    assert 1 == ModeDegree.from_note_pair(note=Note("B3"), base_note=Note("B3"))
    assert 1 == ModeDegree.from_note_pair(note=Note("C3"), base_note=Note("C3"))
    assert 1 == ModeDegree.from_note_pair(note=Note("B-3"), base_note=Note("B-3"))

    assert 2 == ModeDegree.from_note_pair(note=Note("E3"), base_note=Note("D3"))
    assert 2 == ModeDegree.from_note_pair(note=Note("F3"), base_note=Note("E3"))
    assert 2 == ModeDegree.from_note_pair(note=Note("G3"), base_note=Note("F3"))
    assert 2 == ModeDegree.from_note_pair(note=Note("A3"), base_note=Note("G3"))
    assert 2 == ModeDegree.from_note_pair(note=Note("B3"), base_note=Note("A3"))
    assert 2 == ModeDegree.from_note_pair(note=Note("C3"), base_note=Note("B3"))
    assert 2 == ModeDegree.from_note_pair(note=Note("D3"), base_note=Note("C3"))
    assert 2 == ModeDegree.from_note_pair(note=Note("C3"), base_note=Note("B-3"))
    assert "flat-2" == ModeDegree.from_note_pair(note=Note("B-3"), base_note=Note("A3"))

    assert 3 == ModeDegree.from_note_pair(note=Note("F3"), base_note=Note("D3"))
    assert 3 == ModeDegree.from_note_pair(note=Note("G3"), base_note=Note("E3"))
    assert 3 == ModeDegree.from_note_pair(note=Note("A3"), base_note=Note("F3"))
    assert 3 == ModeDegree.from_note_pair(note=Note("B3"), base_note=Note("G3"))
    assert 3 == ModeDegree.from_note_pair(note=Note("C3"), base_note=Note("A3"))
    assert 3 == ModeDegree.from_note_pair(note=Note("D3"), base_note=Note("B3"))
    assert 3 == ModeDegree.from_note_pair(note=Note("E3"), base_note=Note("C3"))
    assert 3 == ModeDegree.from_note_pair(note=Note("D3"), base_note=Note("B-3"))
    assert "flat-3" == ModeDegree.from_note_pair(note=Note("B-3"), base_note=Note("G3"))

    assert 4 == ModeDegree.from_note_pair(note=Note("G3"), base_note=Note("D3"))
    assert 4 == ModeDegree.from_note_pair(note=Note("A3"), base_note=Note("E3"))
    assert 4 == ModeDegree.from_note_pair(note=Note("B3"), base_note=Note("F3"))
    assert 4 == ModeDegree.from_note_pair(note=Note("C3"), base_note=Note("G3"))
    assert 4 == ModeDegree.from_note_pair(note=Note("D3"), base_note=Note("A3"))
    assert 4 == ModeDegree.from_note_pair(note=Note("E3"), base_note=Note("B3"))
    assert 4 == ModeDegree.from_note_pair(note=Note("F3"), base_note=Note("C3"))
    assert 4 == ModeDegree.from_note_pair(note=Note("E3"), base_note=Note("B-3"))
    assert "flat-4" == ModeDegree.from_note_pair(note=Note("B-3"), base_note=Note("F3"))

    assert 5 == ModeDegree.from_note_pair(note=Note("A3"), base_note=Note("D3"))
    assert 5 == ModeDegree.from_note_pair(note=Note("B3"), base_note=Note("E3"))
    assert 5 == ModeDegree.from_note_pair(note=Note("C3"), base_note=Note("F3"))
    assert 5 == ModeDegree.from_note_pair(note=Note("D3"), base_note=Note("G3"))
    assert 5 == ModeDegree.from_note_pair(note=Note("E3"), base_note=Note("A3"))
    assert 5 == ModeDegree.from_note_pair(note=Note("F3"), base_note=Note("B3"))
    assert 5 == ModeDegree.from_note_pair(note=Note("G3"), base_note=Note("C3"))
    assert 5 == ModeDegree.from_note_pair(note=Note("F3"), base_note=Note("B-3"))
    assert "flat-5" == ModeDegree.from_note_pair(note=Note("B-3"), base_note=Note("E3"))

    assert 6 == ModeDegree.from_note_pair(note=Note("B3"), base_note=Note("D3"))
    assert 6 == ModeDegree.from_note_pair(note=Note("C3"), base_note=Note("E3"))
    assert 6 == ModeDegree.from_note_pair(note=Note("D3"), base_note=Note("F3"))
    assert 6 == ModeDegree.from_note_pair(note=Note("E3"), base_note=Note("G3"))
    assert 6 == ModeDegree.from_note_pair(note=Note("F3"), base_note=Note("A3"))
    assert 6 == ModeDegree.from_note_pair(note=Note("G3"), base_note=Note("B3"))
    assert 6 == ModeDegree.from_note_pair(note=Note("A3"), base_note=Note("C3"))
    assert 6 == ModeDegree.from_note_pair(note=Note("G3"), base_note=Note("B-3"))
    assert "flat-6" == ModeDegree.from_note_pair(note=Note("B-3"), base_note=Note("D3"))

    assert 7 == ModeDegree.from_note_pair(note=Note("C3"), base_note=Note("D3"))
    assert 7 == ModeDegree.from_note_pair(note=Note("D3"), base_note=Note("E3"))
    assert 7 == ModeDegree.from_note_pair(note=Note("E3"), base_note=Note("F3"))
    assert 7 == ModeDegree.from_note_pair(note=Note("F3"), base_note=Note("G3"))
    assert 7 == ModeDegree.from_note_pair(note=Note("G3"), base_note=Note("A3"))
    assert 7 == ModeDegree.from_note_pair(note=Note("A3"), base_note=Note("B3"))
    assert 7 == ModeDegree.from_note_pair(note=Note("B3"), base_note=Note("C3"))
    assert 7 == ModeDegree.from_note_pair(note=Note("A3"), base_note=Note("B-3"))
    assert "flat-7" == ModeDegree.from_note_pair(note=Note("B-3"), base_note=Note("C3"))


def test_mode_degrees_from_pc_pairs():
    assert 1 == ModeDegree.from_pc_pair(pc=PC("D"), base_pc=PC("D"))
    assert 1 == ModeDegree.from_pc_pair(pc=PC("E"), base_pc=PC("E"))
    assert 1 == ModeDegree.from_pc_pair(pc=PC("F"), base_pc=PC("F"))
    assert 1 == ModeDegree.from_pc_pair(pc=PC("G"), base_pc=PC("G"))
    assert 1 == ModeDegree.from_pc_pair(pc=PC("A"), base_pc=PC("A"))
    assert 1 == ModeDegree.from_pc_pair(pc=PC("B"), base_pc=PC("B"))
    assert 1 == ModeDegree.from_pc_pair(pc=PC("C"), base_pc=PC("C"))
    assert "#1" == ModeDegree.from_pc_pair(pc=PC("B"), base_pc=PC("B-"))
    assert 1 == ModeDegree.from_pc_pair(pc=PC("B-"), base_pc=PC("B-"))

    assert 2 == ModeDegree.from_pc_pair(pc=PC("E"), base_pc=PC("D"))
    assert 2 == ModeDegree.from_pc_pair(pc=PC("F"), base_pc=PC("E"))
    assert 2 == ModeDegree.from_pc_pair(pc=PC("G"), base_pc=PC("F"))
    assert 2 == ModeDegree.from_pc_pair(pc=PC("A"), base_pc=PC("G"))
    assert 2 == ModeDegree.from_pc_pair(pc=PC("B"), base_pc=PC("A"))
    assert 2 == ModeDegree.from_pc_pair(pc=PC("C"), base_pc=PC("B"))
    assert 2 == ModeDegree.from_pc_pair(pc=PC("D"), base_pc=PC("C"))
    assert 2 == ModeDegree.from_pc_pair(pc=PC("C"), base_pc=PC("B-"))

    assert 3 == ModeDegree.from_pc_pair(pc=PC("F"), base_pc=PC("D"))
    assert 3 == ModeDegree.from_pc_pair(pc=PC("G"), base_pc=PC("E"))
    assert 3 == ModeDegree.from_pc_pair(pc=PC("A"), base_pc=PC("F"))
    assert 3 == ModeDegree.from_pc_pair(pc=PC("B"), base_pc=PC("G"))
    assert 3 == ModeDegree.from_pc_pair(pc=PC("C"), base_pc=PC("A"))
    assert 3 == ModeDegree.from_pc_pair(pc=PC("D"), base_pc=PC("B"))
    assert 3 == ModeDegree.from_pc_pair(pc=PC("E"), base_pc=PC("C"))
    assert 3 == ModeDegree.from_pc_pair(pc=PC("D"), base_pc=PC("B-"))

    assert 4 == ModeDegree.from_pc_pair(pc=PC("G"), base_pc=PC("D"))
    assert 4 == ModeDegree.from_pc_pair(pc=PC("A"), base_pc=PC("E"))
    assert 4 == ModeDegree.from_pc_pair(pc=PC("B"), base_pc=PC("F"))
    assert 4 == ModeDegree.from_pc_pair(pc=PC("C"), base_pc=PC("G"))
    assert 4 == ModeDegree.from_pc_pair(pc=PC("D"), base_pc=PC("A"))
    assert 4 == ModeDegree.from_pc_pair(pc=PC("E"), base_pc=PC("B"))
    assert 4 == ModeDegree.from_pc_pair(pc=PC("F"), base_pc=PC("C"))
    assert 4 == ModeDegree.from_pc_pair(pc=PC("E"), base_pc=PC("B-"))

    assert 5 == ModeDegree.from_pc_pair(pc=PC("A"), base_pc=PC("D"))
    assert 5 == ModeDegree.from_pc_pair(pc=PC("B"), base_pc=PC("E"))
    assert 5 == ModeDegree.from_pc_pair(pc=PC("C"), base_pc=PC("F"))
    assert 5 == ModeDegree.from_pc_pair(pc=PC("D"), base_pc=PC("G"))
    assert 5 == ModeDegree.from_pc_pair(pc=PC("E"), base_pc=PC("A"))
    assert 5 == ModeDegree.from_pc_pair(pc=PC("F"), base_pc=PC("B"))
    assert 5 == ModeDegree.from_pc_pair(pc=PC("G"), base_pc=PC("C"))
    assert 5 == ModeDegree.from_pc_pair(pc=PC("F"), base_pc=PC("B-"))

    assert 6 == ModeDegree.from_pc_pair(pc=PC("B"), base_pc=PC("D"))
    assert 6 == ModeDegree.from_pc_pair(pc=PC("C"), base_pc=PC("E"))
    assert 6 == ModeDegree.from_pc_pair(pc=PC("D"), base_pc=PC("F"))
    assert 6 == ModeDegree.from_pc_pair(pc=PC("E"), base_pc=PC("G"))
    assert 6 == ModeDegree.from_pc_pair(pc=PC("F"), base_pc=PC("A"))
    assert 6 == ModeDegree.from_pc_pair(pc=PC("G"), base_pc=PC("B"))
    assert 6 == ModeDegree.from_pc_pair(pc=PC("A"), base_pc=PC("C"))
    assert 6 == ModeDegree.from_pc_pair(pc=PC("G"), base_pc=PC("B-"))

    assert 7 == ModeDegree.from_pc_pair(pc=PC("C"), base_pc=PC("D"))
    assert 7 == ModeDegree.from_pc_pair(pc=PC("D"), base_pc=PC("E"))
    assert 7 == ModeDegree.from_pc_pair(pc=PC("E"), base_pc=PC("F"))
    assert 7 == ModeDegree.from_pc_pair(pc=PC("F"), base_pc=PC("G"))
    assert 7 == ModeDegree.from_pc_pair(pc=PC("G"), base_pc=PC("A"))
    assert 7 == ModeDegree.from_pc_pair(pc=PC("A"), base_pc=PC("B"))
    assert 7 == ModeDegree.from_pc_pair(pc=PC("B"), base_pc=PC("C"))
    assert 7 == ModeDegree.from_pc_pair(pc=PC("A"), base_pc=PC("B-"))

    assert 1 == ModeDegree.from_pc_pair(pc=PC("B-"), base_pc=PC("B-"))
    assert "#1" == ModeDegree.from_pc_pair(pc=PC("B"), base_pc=PC("B-"))
    assert 2 == ModeDegree.from_pc_pair(pc=PC("C"), base_pc=PC("B-"))
    assert 3 == ModeDegree.from_pc_pair(pc=PC("D"), base_pc=PC("B-"))
    assert 4 == ModeDegree.from_pc_pair(pc=PC("E"), base_pc=PC("B-"))
    assert 5 == ModeDegree.from_pc_pair(pc=PC("F"), base_pc=PC("B-"))
    assert 6 == ModeDegree.from_pc_pair(pc=PC("G"), base_pc=PC("B-"))
    assert 7 == ModeDegree.from_pc_pair(pc=PC("A"), base_pc=PC("B-"))


def test_initialisation_methods():
    md = ModeDegree.from_other(3)
    assert md.value == 3
    assert md.alter == 0

    md1 = ModeDegree.from_pc_pair(pc="A", base_pc="E")
    assert md1.value == 4
    assert md1.alter == 0

    md2 = ModeDegree.from_other(md1)
    assert md2.value == 4
    assert md2.alter == 0

    assert md2 == md1
