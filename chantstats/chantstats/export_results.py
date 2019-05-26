import matplotlib.pyplot as plt
import os

from .logging import logger
from .plotting import get_color_palette_for_unit, plot_pc_freq_distributions, plot_pc_tendency_distributions


__all__ = ["export_results"]


class MissingDendrogramNodesError(Exception):
    """
    Custom exception
    """


def export_stacked_bar_charts_for_pc_freqs(dendrogram, p_cutoff, output_root_dir, result_descriptor):
    nodes_below_cutoff = dendrogram.get_nodes_below_cutoff(p_cutoff)
    if nodes_below_cutoff == []:
        raise MissingDendrogramNodesError()
    color_palette = get_color_palette_for_unit(result_descriptor.unit)
    fig = plot_pc_freq_distributions(nodes_below_cutoff, color_palette=color_palette)
    outfilename = result_descriptor.get_full_output_path(output_root_dir, "stacked_bar_chart.png", p_cutoff=p_cutoff)
    fig.savefig(os.path.join(outfilename))
    plt.close(fig)


def export_stacked_bar_charts_for_pc_tendencies(dendrogram, p_cutoff, output_root_dir, result_descriptor):
    nodes_below_cutoff = dendrogram.get_nodes_below_cutoff(p_cutoff)
    if nodes_below_cutoff == []:
        raise MissingDendrogramNodesError()
    height_per_axes = 2.5
    color_palette = get_color_palette_for_unit(result_descriptor.unit)
    fig, axes = plt.subplots(
        nrows=len(nodes_below_cutoff), ncols=1, figsize=(7, len(nodes_below_cutoff) * height_per_axes)
    )
    if len(nodes_below_cutoff) == 1:
        axes = [axes]
    for ax, node in zip(axes, nodes_below_cutoff):
        plot_pc_tendency_distributions(node, ax=ax, color_palette=color_palette)
    fig.tight_layout()
    outfilename = result_descriptor.get_full_output_path(output_root_dir, "stacked_bar_chart.png", p_cutoff=p_cutoff)
    fig.savefig(outfilename)
    plt.close(fig)


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
    for result_descriptor in results.keys():
        analysis_name = result_descriptor.analysis
        unit = result_descriptor.unit
        assert analysis_name in ["pc_freqs", "pc_tendencies"]

        output_dir = result_descriptor.get_output_dir(output_root_dir, p_cutoff=p_cutoff)
        logger.info(f"Exporting results to folder: {output_dir}")
        dendrogram = results[result_descriptor]["dendrogram"]

        # Export dendrogram
        os.makedirs(output_dir, exist_ok=True)
        fig = dendrogram.plot_dendrogram(p_cutoff=p_cutoff)
        outfilename = result_descriptor.get_full_output_path(output_root_dir, "dendrogram.png", p_cutoff=p_cutoff)
        fig.savefig(outfilename)

        # Export stacked bar chart(s)
        try:
            if analysis_name == "pc_freqs":
                export_stacked_bar_charts_for_pc_freqs(dendrogram, p_cutoff, output_root_dir, result_descriptor)
            elif analysis_name == "pc_tendencies":
                export_stacked_bar_charts_for_pc_tendencies(dendrogram, p_cutoff, output_root_dir, result_descriptor)
            else:
                raise NotImplementedError()
        except MissingDendrogramNodesError:
            msg = f"Cannot plot PC freq distributions: no dendrogram nodes are below p_cutoff={p_cutoff} {result_descriptor}"
            logger.warning(msg)
