import pytest
from .sample_pieces import *

from .context import chantstats
from chantstats.exceptions import UndefinedMainFinal


def test_main_final():
    assert "G" == piece1.main_final
    assert "D" == piece2.main_final
    assert "C" == piece5.main_final
    assert "D" == piece7.main_final
    assert "G" == piece14.main_final
    assert "C" == piece45.main_final


@pytest.mark.parametrize("piece", [piece3, piece4, piece6, piece12])
def test_main_final_undefined_for_heavy_polymodal_frame_pieces(piece):

    with pytest.raises(UndefinedMainFinal, match="Main final undefined"):
        piece.main_final
