import os
import pytest
import sh
from approvaltests.approvals import verify

from .context import chantstats
from chantstats import ChantStatsConfig, calculate_results, export_results, logger

chants_dir = os.environ["CHANTS_DIR"]


@pytest.mark.slow
def test_run_pc_freqs_analysis(tmpdir, diff_reporter):
    output_root_dir = os.getenv("CHANTSTATS_OUTPUT_ROOT_DIR", str(tmpdir))
    logger.info(f"Using output root dir: '{output_root_dir}'")

    cfg = ChantStatsConfig(musicxml_paths={"plainchant_sequences": chants_dir})
    repertoire_and_genre = "plainchant_sequences"
    analysis_name = "pc_freqs"
    min_length_monomodal_sections = 3

    results = calculate_results(
        repertoire_and_genre, analysis_name, cfg, min_length_monomodal_sections=min_length_monomodal_sections
    )
    export_results(results, output_root_dir, p_cutoff=0.7)

    exported_files = sh.tail(sh.tree(output_root_dir), "-n", "+2").stdout.decode("utf8")
    verify(exported_files, diff_reporter)