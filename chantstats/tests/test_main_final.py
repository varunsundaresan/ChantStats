from .sample_pieces import *


def test_main_final():
    assert "G" == piece1.main_final
    assert "D" == piece2.main_final
    assert "C" == piece5.main_final
    assert "D" == piece7.main_final
    assert "D" == piece8.main_final
    assert "G" == piece14.main_final
    assert "C" == piece45.main_final


def test_main_final_is_None_for_heavy_polymodal_frame_pieces():
    assert None == piece3.main_final
    assert None == piece4.main_final
    assert None == piece6.main_final
    assert None == piece12.main_final
