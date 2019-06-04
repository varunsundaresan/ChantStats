import matplotlib.pyplot as plt
import os
from .color_palettes import get_color_palette_for_unit
from .dendrogram.plotting import (
    plot_pc_freq_distributions,
    plot_tendency_distributions,
    plot_LMO_freq_distributions,
    plot_tendency_distribution_NEW,
)
from .logging import logger
from .utils import plot_empty_figure


class MissingDendrogramNodesError(Exception):
    """
    Custom exception
    """


def export_empty_figure(output_root_dir, result_descriptor):
    # raise NotImplementedError("TODO: implement this if required")
    msg_text = "This plot is deliberately empty\nbecause there is no data to export."
    fig = plot_empty_figure(msg_text, result_descriptor=result_descriptor, figsize=(22, 4))
    outfilename = result_descriptor.get_full_output_path(
        output_root_dir, filename_prefix="stacked_bar_chart", filename_suffix=""
    )
    fig.savefig(outfilename)
    return fig


# def export_stacked_bar_chart_for_pc_freqs_OLD(nodes_below_cutoff, output_root_dir, result_descriptor):
#     assert len(nodes_below_cutoff) > 0
#     color_palette = get_color_palette_for_unit(result_descriptor.unit)
#     fig = plot_pc_freq_distributions(
#         nodes_below_cutoff, result_descriptor=result_descriptor, color_palette=color_palette
#     )
#     fig.tight_layout()
#     outfilename = result_descriptor.get_full_output_path(
#         output_root_dir, filename_prefix="stacked_bar_chart", filename_suffix=""
#     )
#     fig.savefig(outfilename)
#     plt.close(fig)


def export_stacked_bar_chart_for_pc_freqs(nodes_below_cutoff, output_root_dir, result_descriptor):
    assert len(nodes_below_cutoff) > 0
    color_palette = get_color_palette_for_unit(result_descriptor.unit)
    figs = plot_pc_freq_distributions(
        nodes_below_cutoff, result_descriptor=result_descriptor, color_palette=color_palette
    )
    num_figs = len(figs)
    for i, fig in enumerate(figs, start=1):
        outfilename = result_descriptor.get_full_output_path(
            output_root_dir, filename_prefix="stacked_bar_chart", filename_suffix=f"__{i:02d}_of_{num_figs:02d}"
        )
        fig.savefig(outfilename)


def export_stacked_bar_chart_for_tendency(nodes_below_cutoff, output_root_dir, result_descriptor, height_per_axes=2.5):
    assert len(nodes_below_cutoff) > 0
    color_palette = get_color_palette_for_unit(result_descriptor.unit)
    fig, axes = plt.subplots(
        nrows=len(nodes_below_cutoff), ncols=1, figsize=(7, len(nodes_below_cutoff) * height_per_axes)
    )
    if len(nodes_below_cutoff) == 1:
        axes = [axes]
    for ax, node in zip(axes, nodes_below_cutoff):
        plot_tendency_distributions(node, result_descriptor=result_descriptor, ax=ax, color_palette=color_palette)
    fig.tight_layout()
    outfilename = result_descriptor.get_full_output_path(
        output_root_dir, filename_prefix="stacked_bar_chart", filename_suffix=""
    )
    fig.savefig(outfilename)
    plt.close(fig)


def export_individual_stacked_bar_charts_for_tendency(nodes_below_cutoff, output_root_dir, result_descriptor):
    assert len(nodes_below_cutoff) > 0
    color_palette = get_color_palette_for_unit(result_descriptor.unit)

    for idx, node in enumerate(nodes_below_cutoff, start=1):
        fig = plot_tendency_distributions(node, result_descriptor=result_descriptor, color_palette=color_palette)
        fig.tight_layout()
        outfilename = result_descriptor.get_full_output_path(
            output_root_dir, filename_prefix="stacked_bar_chart", filename_suffix=f"{idx:02d}"
        )
        fig.savefig(outfilename)
        plt.close(fig)


def export_stacked_bar_chart_for_modal_category_tendency(distribution, output_root_dir, result_descriptor):
    color_palette = get_color_palette_for_unit(result_descriptor.unit)
    fig = plot_tendency_distribution_NEW(distribution, result_descriptor=result_descriptor, color_palette=color_palette)
    fig.tight_layout()
    outfilename = result_descriptor.get_full_output_path(
        output_root_dir, filename_prefix="stacked_bar_chart", filename_suffix=""
    )
    fig.savefig(outfilename)
    plt.close(fig)


def export_stacked_bar_chart_for_leaps_and_melodic_outlines(nodes_below_cutoff, output_root_dir, result_descriptor):
    assert len(nodes_below_cutoff) > 0
    color_palette = get_color_palette_for_unit(result_descriptor.unit)
    figs = plot_LMO_freq_distributions(
        nodes_below_cutoff, result_descriptor=result_descriptor, color_palette=color_palette
    )
    num_figs = len(figs)
    for i, fig in enumerate(figs, start=1):
        outfilename = result_descriptor.get_full_output_path(
            output_root_dir, filename_prefix="stacked_bar_chart", filename_suffix=f"__{i:02d}_of_{num_figs:02d}"
        )
        fig.savefig(outfilename)


# def export_stacked_bar_chart_for_leaps_and_melodic_outlines_OLD(nodes_below_cutoff, output_root_dir, result_descriptor):
#     assert len(nodes_below_cutoff) > 0
#     color_palette = get_color_palette_for_unit(result_descriptor.unit)
#     fig = plot_LMO_freq_distributions(
#         nodes_below_cutoff, result_descriptor=result_descriptor, color_palette=color_palette
#     )
#     outfilename = result_descriptor.get_full_output_path(
#         output_root_dir, filename_prefix="stacked_bar_chart", filename_suffix=""
#     )
#     fig.savefig(outfilename)
#     plt.close(fig)


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
    # Tweak output root folder
    p_cutoff_path_stub = f"p_cutoff_{p_cutoff:.2f}"
    output_root_dir = os.path.join(output_root_dir, p_cutoff_path_stub)

    for result_descriptor in results.keys():
        output_dir = result_descriptor.get_output_dir(output_root_dir)
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Exporting results to folder: {output_dir}")

        if result_descriptor.analysis == "tendency":
            distribution = results[result_descriptor]["tendency_distribution"]
            export_stacked_bar_chart_for_modal_category_tendency(distribution, output_root_dir, result_descriptor)
        else:
            # Export dendrogram
            dendrogram = results[result_descriptor]["dendrogram"]
            fig = dendrogram.plot_dendrogram(p_cutoff=p_cutoff, result_descriptor=result_descriptor)
            outfilename = result_descriptor.get_full_output_path(
                output_root_dir, filename_prefix="dendrogram", filename_suffix=""
            )
            fig.savefig(outfilename)

            # Export stacked bar chart(s)
            nodes_below_cutoff = dendrogram.get_nodes_below_cutoff(
                p_cutoff, include_leaf_nodes=include_leaf_nodes_in_clusters
            )
            if nodes_below_cutoff == []:
                msg = f"Exporting empty figure because no dendrogram nodes are below p_cutoff={p_cutoff} {result_descriptor}."
                logger.warning(msg)
                export_empty_figure(output_root_dir, result_descriptor)
                continue

            if result_descriptor.analysis == "pc_freqs":
                export_stacked_bar_chart_for_pc_freqs(nodes_below_cutoff, output_root_dir, result_descriptor)
            # elif result_descriptor.analysis == "tendency":
            #     # export_stacked_bar_charts_for_tendency(nodes_below_cutoff, output_root_dir, result_descriptor)
            #     # export_individual_stacked_bar_charts_for_tendency(nodes_below_cutoff, output_root_dir, result_descriptor)
            elif result_descriptor.analysis == "L_and_M__L5_u_M5" or result_descriptor.analysis == "L_and_M__L4_u_M4":
                export_stacked_bar_chart_for_leaps_and_melodic_outlines(
                    nodes_below_cutoff, output_root_dir, result_descriptor
                )
            else:
                raise NotImplementedError()
