import pytest
from .context import chantstats
from chantstats.v2.ambitus import calculate_ambitus
from unittest.mock import Mock
from music21.note import Note


def test_calculate_ambitus():
    piece = Mock(lowest_note=Note("D3"), note_of_final=None)
    assert calculate_ambitus(piece) == "undefined"
    piece = Mock(lowest_note=Note("C3"), note_of_final=Note("E3"))
    assert calculate_ambitus(piece) == "authentic"
    piece = Mock(lowest_note=Note("D3"), note_of_final=Note("G3"))
    assert calculate_ambitus(piece) == "plagal"

    piece = Mock(lowest_note=Note("F3"), note_of_final=Note("F4"))
    assert calculate_ambitus(piece) == "plagal"

    with pytest.raises(Exception, match="We expect the lowest note to be less than an octave below the main final"):
        piece = Mock(lowest_note=Note("D3"), note_of_final=Note("G4"))
        calculate_ambitus(piece)

    with pytest.raises(Exception, match="We expect the lowest note to be less than an octave below the main final"):
        piece = Mock(lowest_note=Note("F4"), note_of_final=Note("C3"))
        calculate_ambitus(piece)
