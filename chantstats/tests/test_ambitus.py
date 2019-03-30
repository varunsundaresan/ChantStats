from .context import chantstats
from chantstats.plainchant_sequence_piece import AmbitusType

from .sample_pieces import *


def test_ambitus():
    assert "authentic" == piece1.ambitus
    assert "plagal" == piece2.ambitus
    assert "plagal" == piece5.ambitus
    assert "authentic" == piece7.ambitus
    assert "authentic" == piece8.ambitus
    assert (
        "plagal" == piece14.ambitus
    )  # TODO: the amen formula is a lot lower than the rest of the piece; discuss with AVY
    assert "plagal" == piece45.ambitus


def test_ambitus_is_None_for_heavy_polymodal_frame_pieces():
    assert "undefined" == piece3.ambitus
    assert "undefined" == piece4.ambitus
    assert "undefined" == piece6.ambitus
    assert "undefined" == piece12.ambitus
