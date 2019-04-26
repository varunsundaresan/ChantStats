import os
import palettable
import shutil

from chantstats.unit import UnitType
from .dendrogram2 import Dendrogram
from .logging import logger

__all__ = ["export_dendrogram_and_stacked_bar_chart"]


def get_color_palette_for_unit(unit):
    unit = UnitType(unit)
    if unit.value == "pcs":
        return palettable.cartocolors.qualitative.Vivid_8.hex_colors
    elif unit.value == "mode_degrees":
        return palettable.cartocolors.qualitative.Pastel_10.hex_colors
        # return palettable.colorbrewer.qualitative.Set3_12.hex_colors
    else:
        raise ValueError(f"Unexpected value: {unit.value}")


def export_dendrogram_and_stacked_bar_chart(
    *, output_root_dir, analysis_spec, modal_category, p_cutoff, unit, sort_freqs_ascending=False, overwrite=False
):
    """
    Export dendrogram and stacked bar chart for this modal category.

    Parameters
    ----------
    output_root_dir : str
        The path under which to export results. Note that the actual directory
        where the plots are saved will be a sub-directory of this root directory,
        for example: `<output_root_dir>/authentic_modes/G_authentic`.
    analysis_spec : FullAnalysisSpec
    modal_cagetory : ModalCategory
    p_cutoff : float
    unit : UnitType
    sort_freqs_ascending : bool, optional
    overwrite: book, optional
    """
    logger.info(f"Exporting results for analysis_spec={analysis_spec}, modal_category={modal_category}, unit='{unit}'")

    output_dir = analysis_spec.output_path(root_dir=output_root_dir, modal_category=modal_category, unit=unit)
    if os.path.exists(output_dir):
        if not overwrite:
            logger.warning(
                f"Output directory exists. Use `overwrite=True` to delete its contents before exporting results: '{output_dir}'"
            )
            return
        else:
            logger.warning(f"Deleting contents of existing output directory (because overwrite=True): '{output_dir}'")
            shutil.rmtree(output_dir)
    if not os.path.exists(output_dir):
        logger.debug(f"Creating output dir: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

    df = modal_category.make_results_dataframe(analysis_func=analysis_spec.analysis_func, unit=unit)
    dendrogram = Dendrogram(df, p_threshold=p_cutoff)

    output_filename = os.path.join(output_dir, "dendrogram.png")
    title = f"Dendrogram: {analysis_spec.get_description(modal_category=modal_category)} (p_cutoff={p_cutoff}, unit='{unit}')"
    fig = dendrogram.plot_dendrogram(title=title)
    fig.savefig(output_filename)
    logger.debug(f"Saved dendrogram plot: '{output_filename}'")

    output_filename = os.path.join(output_dir, "stacked_bar_chart.png")
    title = f"{analysis_spec.get_description(modal_category=modal_category)} (p_cutoff={p_cutoff}, unit='{unit}')"

    color_palette = get_color_palette_for_unit(unit)
    fig = dendrogram.plot_stacked_bar_charts(
        title=title, sort_freqs_ascending=sort_freqs_ascending, color_palette=color_palette
    )
    fig.savefig(output_filename)
    logger.debug(f"Saved stacked bar chart: '{output_filename}'")
