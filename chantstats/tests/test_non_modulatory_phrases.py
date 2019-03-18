from .sample_pieces import *


def test_non_modulatory_phrases():
    """
    Check the number of non-modulatory phrases for a few pieces.
    """
    assert len(piece1.non_modulatory_phrases) == 3
    assert len(piece2.non_modulatory_phrases) == 14
    assert len(piece5.non_modulatory_phrases) == 13
    assert len(piece7.non_modulatory_phrases) == 19
    assert len(piece8.non_modulatory_phrases) == 14
    assert len(piece14.non_modulatory_phrases) == 26
    assert len(piece45.non_modulatory_phrases) == 20


def test_list_of_non_modulatory_phrases_is_empty_for_pieces_with_heavy_polymodal_frame():
    """
    Check that for pieces with a heavy polymodal frame the list of non-modulatory phrases is empty.
    """
    assert piece3.non_modulatory_phrases == []
    assert piece4.non_modulatory_phrases == []
