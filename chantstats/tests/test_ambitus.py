from .context import chantstats
from chantstats.ambitus import AmbitusType

from .sample_pieces import *


def test_ambitus():
    assert "authentic" == piece1.ambitus
    assert "plagal" == piece2.ambitus
    assert "plagal" == piece5.ambitus
    assert "authentic" == piece7.ambitus
    assert "authentic" == piece8.ambitus
    assert "plagal" == piece14.ambitus  # TODO: the amen formula is a lot lower than the rest of the piece;
    # discuss with AVY whether this should affect ambitus calculation for light polymodal pieces in case the
    # piece without the amen formula would be considered authentic but with the amen formula is plagal.
    assert "plagal" == piece45.ambitus


def test_ambitus_is_None_for_heavy_polymodal_frame_pieces():
    assert "undefined" == piece3.ambitus
    assert "undefined" == piece4.ambitus
    assert "undefined" == piece6.ambitus
    assert "undefined" == piece12.ambitus


def test_ambitus_of_monomodal_sections():
    assert "authentic" == piece1.get_monomodal_sections(enforce_same_ambitus=False)[0].ambitus
    assert "plagal" == piece2.get_monomodal_sections(enforce_same_ambitus=False)[0].ambitus
    assert "authentic" == piece4.get_monomodal_sections(enforce_same_ambitus=False)[0].ambitus
    assert "plagal" == piece4.get_monomodal_sections(enforce_same_ambitus=False)[1].ambitus
    assert "plagal" == piece5.get_monomodal_sections(enforce_same_ambitus=False)[0].ambitus
