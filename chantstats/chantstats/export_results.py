import os
import shutil

from .analysis_spec import AnalysisType
from .logging import logger
from .plotting import get_color_palette_for_unit, plot_pc_freq_distributions
from .unit import UnitType

__all__ = ["export_results"]


def export_results(results, output_root_dir, p_cutoff=0.7, overwrite=False):
    """
    Export analysis results as dendrogram plots and stacked bar charts
    into a folder hierarchy underneath output_root_dir.

    Parameters
    ----------
    results : dict
        Analysis results (as a dictionary of the form {path_stubs: {'dendrogram': <dendrogram>}}).
    output_root_dir : str
        Path to the root directory under which the results will be exported.
    p_cutoff : float
        Cutoff value that determines which dendrogram nodes are exported.
    overwrite : bool
        If True, delete the output root folder (if it exists) before exporting results. Default: False.
    """
    if os.path.exists(output_root_dir):
        if not overwrite:
            logger.warn(f"Aborting because output root dir already exists: '{output_root_dir}'")
            logger.warn(f"Use 'overwrite=True' to overwrite existing results.")
            return
        else:
            logger.warn(f"Removing existing output root dir: {output_root_dir}")
            shutil.rmtree(output_root_dir)

    for path_stubs in results.keys():
        analysis_name = path_stubs.analysis
        unit = path_stubs.unit
        assert analysis_name == "pc_freqs"

        path_stub_p_cutoff = f"p_cutoff_{p_cutoff:.2f}"
        extra_path_stubs = [path_stub_p_cutoff]
        output_dir = os.path.join(output_root_dir, *extra_path_stubs, *path_stubs)
        logger.info(f"Exporting results to folder: {output_dir}")
        dendrogram = results[path_stubs]["dendrogram"]

        # Export dendrogram
        os.makedirs(output_dir, exist_ok=True)
        fig = dendrogram.plot_dendrogram(p_cutoff=p_cutoff)
        fig.savefig(os.path.join(output_dir, "dendrogram.png"))

        # Export stacked bar chart(s)
        nodes_below_cutoff = dendrogram.get_nodes_below_cutoff(p_cutoff)
        if nodes_below_cutoff == []:
            msg = f"Cannot plot PC freq distributions: no dendrogram nodes are below p_cutoff={p_cutoff} {path_stubs}"
            logger.warning(msg)
            continue
        color_palette = get_color_palette_for_unit(unit)
        fig = plot_pc_freq_distributions(nodes_below_cutoff, color_palette=color_palette)
        fig.savefig(os.path.join(output_dir, "stacked_bar_chart.png"))
