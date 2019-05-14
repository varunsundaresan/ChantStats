import os
import pytest
from approvaltests.approvals import verify

from .context import chantstats
from chantstats import load_plainchant_sequence_pieces, FullAnalysisSpec, GroupingByModalCategory
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


@pytest.mark.slow
def test_results_folder_structure(tmpdir, diff_reporter):
    output_root_dir = str(tmpdir)
    print(f"[DDD] output_root_dir={output_root_dir}")
    pieces = load_plainchant_sequence_pieces(
        chants_dir, pattern="BN_lat_1112_Sequence_*.xml", exclude_heavy_polymodal_frame_pieces=False
    )
    monomodal_sections = sum([p.get_monomodal_sections(min_length=3) for p in pieces], [])
    analysis_spec = FullAnalysisSpec(repertoire_and_genre="plainchant_sequences", analysis="pc_freqs", unit="pcs")
    group_by = "final"
    grouping = GroupingByModalCategory(monomodal_sections, group_by=group_by)
    grouping.export_results(
        output_root_dir=output_root_dir,
        analysis_spec=analysis_spec,
        p_cutoff=0.7,
        overwrite=True,
        sort_freqs_ascending=False,
    )
    output_folder_structure = list_directory_tree(output_root_dir)
    verify(output_folder_structure, diff_reporter)
