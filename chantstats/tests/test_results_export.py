import pytest

from .context import chantstats
from chantstats import FullAnalysisSpec


@pytest.mark.parametrize(
    "repertoire_and_genre, analysis, unit, mode, final, output_path_expected",
    [
        (
            "plainchant_sequences",
            "pc_freqs",
            "pcs",
            "by_final",
            "D",
            "/foobar/chant/pc_freqs/sequences/pcs/by_final/D_final",
        ),
        (
            "responsorial_chants",
            "tendency",
            "mode_degrees",
            "authentic_modes",
            "G",
            "/foobar/chant/tendency/responsorial_chants/mode_degrees/authentic_modes/G_authentic",
        ),
        (
            "organa",
            "approaches_and_departures",
            "pcs",
            "plagal_modes",
            "C",
            "/foobar/organum/approaches_and_departures/pcs/plagal_modes/C_plagal",
        ),
    ],
)
def test_output_path(repertoire_and_genre, analysis, unit, mode, final, output_path_expected):
    """
    Analysis spec returns the expected output path, depending on its input parameters.
    """
    spec = FullAnalysisSpec(repertoire_and_genre=repertoire_and_genre, analysis=analysis, unit=unit, mode=mode)
    output_path = spec.output_path(root_dir="/foobar", final=final)
    assert output_path_expected == output_path
