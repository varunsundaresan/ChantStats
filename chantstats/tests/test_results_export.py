import os
import pytest
from approvaltests.approvals import verify

from .context import chantstats
from chantstats import (
    load_pieces,
    load_plainchant_sequence_pieces,
    FullAnalysisSpec,
    GroupingByModalCategory,
    ChantStatsConfig,
)
from chantstats.utils import list_directory_tree


try:
    chants_dir = os.environ["CHANTS_DIR"]
except KeyError:
    raise RuntimeError("The environment variable CHANTS_DIR must be defined to run the tests.")


@pytest.mark.skip(
    reason="This test needs to be rewritten once the analysis spec and modal category refactoring is complete."
)
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
            "pc_tendencies",
            "mode_degrees",
            "authentic_modes",
            "G",
            "/foobar/chant/pc_tendencies/responsorial_chants/mode_degrees/authentic_modes/G_authentic",
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
    spec = FullAnalysisSpec(repertoire_and_genre=repertoire_and_genre, analysis=analysis, unit=unit)
    # modal_category = ModalCategory(items=[], ...)
    # output_path = spec.output_path(root_dir="/foobar", modal_category=...)
    # assert output_path_expected == output_path
    assert False


@pytest.mark.skip(reason="This test is obsolete and superseded by 'test_run_pc_freqs_analysis_and_export_results'")
@pytest.mark.slow
def test_results_folder_structure(tmpdir, diff_reporter):
    output_root_dir = str(tmpdir)
    print(f"[DDD] output_root_dir={output_root_dir}")
    cfg = ChantStatsConfig(musicxml_paths={"plainchant_sequences": chants_dir})
    pieces = load_pieces(repertoire_and_genre="plainchant_sequences", cfg=cfg)
    monomodal_sections = pieces.get_analysis_inputs(mode="final", min_length_monomodal_sections=3)
    analysis_spec = FullAnalysisSpec(repertoire_and_genre="plainchant_sequences", analysis="pc_freqs")
    group_by = "final"
    grouping = GroupingByModalCategory(monomodal_sections, group_by=group_by)
    grouping.export_results(
        output_root_dir=output_root_dir,
        analysis_spec=analysis_spec,
        p_cutoff=0.7,
        unit="pcs",
        overwrite=True,
        sort_freqs_ascending=False,
    )
    output_folder_structure = list_directory_tree(output_root_dir)
    verify(output_folder_structure, diff_reporter)
