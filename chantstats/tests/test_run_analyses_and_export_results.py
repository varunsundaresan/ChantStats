import os
import pytest
import sh
from approvaltests.approvals import verify

from .context import chantstats
from chantstats import ChantStatsConfig, calculate_results, export_results, logger
from chantstats.utils import list_directory_tree

try:
    chants_dir = os.environ["CHANTS_DIR"]
except KeyError:
    raise RuntimeError("The environment variable CHANTS_DIR must be defined to run the tests.")


@pytest.mark.slow
def test_run_analyses_and_export_results(tmpdir, diff_reporter):
    output_root_dir = os.getenv("CHANTSTATS_OUTPUT_ROOT_DIR", str(tmpdir))
    logger.info(f"Using output root dir: '{output_root_dir}'")

    cfg = ChantStatsConfig(musicxml_paths={"plainchant_sequences": chants_dir})
    repertoire_and_genre = "plainchant_sequences"
    min_length_monomodal_sections = 3

    # Calculate results for PC frequencies
    results_pc_freqs = calculate_results(
        repertoire_and_genre,
        analysis_name="pc_freqs",
        cfg=cfg,
        min_length_monomodal_sections=min_length_monomodal_sections,
    )

    # Calculate results for PC tendencies
    results_pc_tendencies = calculate_results(
        repertoire_and_genre,
        analysis_name="pc_tendencies",
        units=["pcs"],
        cfg=cfg,
        min_length_monomodal_sections=min_length_monomodal_sections,
    )

    # Export all results
    for p_cutoff in [0.7, 0.15]:
        export_results(results_pc_freqs, output_root_dir, p_cutoff=p_cutoff)
        export_results(results_pc_tendencies, output_root_dir, p_cutoff=p_cutoff)

    exported_files = list_directory_tree(output_root_dir)
    verify(exported_files, diff_reporter)
