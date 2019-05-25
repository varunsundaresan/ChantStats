import matplotlib.pyplot as plt
import os
import shutil
from .color_palettes import get_color_palette_for_unit
from .dendrogram.plotting import plot_pc_freq_distributions, plot_tendency_distributions
from .logging import logger


class MissingDendrogramNodesError(Exception):
    """
    Custom exception
    """


def export_empty_figure(output_dir, unit):
    raise NotImplementedError("TODO: implement this if required")
    # fig, ax = plt.subplots(figsize=(20, 4))
    # msg = "This plot is deliberately empty\nbecause there is no data to export."
    # fig.text(0.5, 0.5, msg, fontsize=30, color='gray', ha='center', va='center', alpha=0.5)
    # fig.savefig(os.path.join(output_dir, "stacked_bar_chart.png"))
    # plt.close(fig)
    # return fig


def export_stacked_bar_charts_for_pc_freqs(nodes_below_cutoff, path_stubs, output_dir, unit):
    assert len(nodes_below_cutoff) > 0
    color_palette = get_color_palette_for_unit(unit)
    fig = plot_pc_freq_distributions(nodes_below_cutoff, path_stubs=path_stubs, color_palette=color_palette)
    fig.savefig(os.path.join(output_dir, "stacked_bar_chart.png"))
    plt.close(fig)


def export_stacked_bar_charts_for_tendency(nodes_below_cutoff, path_stubs, output_dir, unit, height_per_axes=2.5):
    assert len(nodes_below_cutoff) > 0
    color_palette = get_color_palette_for_unit(unit)
    fig, axes = plt.subplots(
        nrows=len(nodes_below_cutoff), ncols=1, figsize=(7, len(nodes_below_cutoff) * height_per_axes)
    )
    if len(nodes_below_cutoff) == 1:
        axes = [axes]
    for ax, node in zip(axes, nodes_below_cutoff):
        plot_tendency_distributions(node, ax=ax, color_palette=color_palette)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "stacked_bar_chart.png"))
    plt.close(fig)


def export_results(results, output_root_dir, p_cutoff=0.4, include_leaf_nodes_in_clusters=True, overwrite=False):
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
    include_leaf_nodes_in_clusters : bool
        If True, include all clusters in the results, even those containing only contain a single
        leaf node. Otherwise include only proper clusters (with at least two leaf nodes). Default: True.
    overwrite : bool
        If True, delete the output root folder (if it exists) before exporting results. Default: False.
    """
    # if os.path.exists(output_root_dir):
    #     if not overwrite:
    #         logger.warn(f"Aborting because output root dir already exists: '{output_root_dir}'")
    #         logger.warn(f"Use 'overwrite=True' to overwrite existing results.")
    #         return
    #     else:
    #         logger.warn(f"Removing existing output root dir: {output_root_dir}")
    #         shutil.rmtree(output_root_dir)

    for path_stubs in results.keys():
        analysis_name = path_stubs.analysis
        unit = path_stubs.unit
        assert analysis_name in ["pc_freqs", "tendency"]

        path_stub_p_cutoff = f"p_cutoff_{p_cutoff:.2f}"
        extra_path_stubs = [path_stub_p_cutoff]
        output_dir = os.path.join(output_root_dir, *extra_path_stubs, *path_stubs)

        if os.path.exists(output_dir):
            if overwrite:
                logger.warn(f"Removing existing output folder: {output_dir}")
                shutil.rmtree(output_dir)
            else:
                logger.warning(f"Aborting because output folder already exists: {output_dir}")
                return

        logger.info(f"Exporting results to folder: {output_dir}")
        dendrogram = results[path_stubs]["dendrogram"]

        # Export dendrogram
        os.makedirs(output_dir, exist_ok=True)
        fig = dendrogram.plot_dendrogram(p_cutoff=p_cutoff)
        fig.savefig(os.path.join(output_dir, "dendrogram.png"))

        # Export stacked bar chart(s)
        nodes_below_cutoff = dendrogram.get_nodes_below_cutoff(
            p_cutoff, include_leaf_nodes=include_leaf_nodes_in_clusters
        )
        if nodes_below_cutoff == []:
            msg = f"Exporting empty figure because no dendrogram nodes are below p_cutoff={p_cutoff} {path_stubs}."
            logger.warning(msg)
            export_empty_figure(output_dir, unit)
            continue

        if analysis_name == "pc_freqs":
            export_stacked_bar_charts_for_pc_freqs(nodes_below_cutoff, path_stubs, output_dir, unit)
        elif analysis_name == "tendency":
            export_stacked_bar_charts_for_tendency(nodes_below_cutoff, path_stubs, output_dir, unit)
        else:
            raise NotImplementedError()
