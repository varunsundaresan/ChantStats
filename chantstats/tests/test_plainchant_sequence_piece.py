import os
import pytest
from chantstats.plainchant_sequence_piece import load_plainchant_sequence_pieces

try:
    chants_dir = os.environ["CHANTS_DIR"]
except KeyError:
    raise RuntimeError("The environment variable CHANTS_DIR must be defined to run the tests.")


@pytest.mark.slow
def test_load_plainchant_sequence_pieces():
    filename_pattern = "3[1-3]*.xml"
    pieces = load_plainchant_sequence_pieces(chants_dir, pattern=filename_pattern)
    pieces_expected = ["31_Heri_mundus_exultauit.xml", "32_Magnus_deus.xml", "33_Gratulemur_ad_fastiuum.xml"]
    assert pieces_expected == [p.filename_short for p in pieces]

    # When excluding piece with heavy polymodal frames we expect `32_Magnus_deus.xml` to be missing
    pieces = load_plainchant_sequence_pieces(
        chants_dir, pattern=filename_pattern, exclude_heavy_polymodal_frame_pieces=True
    )
    pieces_expected = ["31_Heri_mundus_exultauit.xml", "33_Gratulemur_ad_fastiuum.xml"]
    assert pieces_expected == [p.filename_short for p in pieces]
