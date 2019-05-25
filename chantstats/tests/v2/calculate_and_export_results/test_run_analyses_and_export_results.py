import os
import pytest
from approvaltests.approvals import verify

from .context import chantstats
from chantstats.v2 import ChantStatsConfig, calculate_results, export_results, logger
from chantstats.v2.utils import list_directory_tree


@pytest.mark.slow
def test_run_analyses_and_export_results(tmpdir, diff_reporter):
    output_root_dir = os.getenv("CHANTSTATS_OUTPUT_ROOT_DIR", str(tmpdir))
    logger.info(f"Using output root dir: '{output_root_dir}'")

    cfg = ChantStatsConfig.from_env()
    repertoire_and_genre = "plainchant_sequences"
    min_num_phrases_per_monomodal_section = 3

    # Calculate results for PC frequencies
    results_pc_freqs = calculate_results(
        repertoire_and_genre,
        analysis="pc_freqs",
        cfg=cfg,
        min_num_phrases_per_monomodal_section=min_num_phrases_per_monomodal_section,
    )

    # Calculate results for PC tendencies
    results_pc_tendencies = calculate_results(
        repertoire_and_genre,
        analysis="pc_tendencies",
        cfg=cfg,
        min_num_phrases_per_monomodal_section=min_num_phrases_per_monomodal_section,
    )

    # Export all results
    for p_cutoff in [0.4]:
        export_results(results_pc_freqs, output_root_dir, p_cutoff=p_cutoff)
        export_results(results_pc_tendencies, output_root_dir, p_cutoff=p_cutoff)

    exported_files = list_directory_tree(output_root_dir)
    verify(exported_files, diff_reporter)
