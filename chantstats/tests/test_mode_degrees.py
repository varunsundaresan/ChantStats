from .sample_pieces import piece1, piece5


def test_mode_degrees_for_phrase():
    """
    Test that mode degrees for selected phrases are as expected.
    """
    assert [3, 5, 6, 3, 1, 1, 2, 4, 3, 2, 1, 3, 1, 2, 1] == piece1.phrases[0].mode_degrees
    assert [6, 6, 7, 1, 1, 7, 2, 4, 3, 3, 1, 3, 1, 2, 7, 6, 1, 1] == piece1.phrases[2].mode_degrees

    expected_mode_degrees = [1, 1, 7, 6, 5, 5, 6, 1, 2, "flat-7", 1, 1, 1, 2, 3, 3, 2, 4, 4, 2, 3, 1, 2, 1, 2, 3, 2, 1]
    assert expected_mode_degrees == piece5.phrases[4].mode_degrees


def test_occurring_mode_degrees():
    occurring_mode_degrees = sorted(set(piece5.phrases[4].mode_degrees))
    expected_mode_degrees = [1, 2, 3, 4, 5, 6, "flat-7", 7]
    assert occurring_mode_degrees == expected_mode_degrees
