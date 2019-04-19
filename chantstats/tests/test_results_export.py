import pytest

from .context import chantstats
from chantstats import FullAnalysisSpec


@pytest.mark.parametrize(
    "repertoire_and_genre, analysis, unit, mode, output_path_expected",
    [
        ("plainchant_sequences", "pc_freqs", "pcs", "by_final", "/foobar/chant/pc_freqs/sequences/pcs/by_final"),
        (
            "responsorial_chants",
            "tendency",
            "mode_degrees",
            "authentic_modes",
            "/foobar/chant/tendency/responsorial_chants/mode_degrees/authentic_modes",
        ),
        (
            "organa",
            "approaches_and_departures",
            "pcs",
            "plagal_modes",
            "/foobar/organum/approaches_and_departures/pcs/plagal_modes",
        ),
    ],
)
def test_output_path(repertoire_and_genre, analysis, unit, mode, output_path_expected):
    """
    Analysis spec returns the expected output path, depending on its input parameters.
    """
    spec = FullAnalysisSpec(repertoire_and_genre=repertoire_and_genre, analysis=analysis, unit=unit, mode=mode)
    output_path = spec.output_path(root_dir="/foobar")
    assert output_path_expected == output_path
