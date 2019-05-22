import matplotlib.pyplot as plt
import numpy as np
import palettable
import pandas as pd
from matplotlib.patches import Patch
from ..unit import UnitType

__all__ = ["plot_stacked_bar_chart_for_relative_pc_frequencies"]


def get_color_palette_for_unit(unit):
    unit = UnitType(unit)
    if unit.value == "pcs":
        return palettable.cartocolors.qualitative.Vivid_8.hex_colors
    elif unit.value == "mode_degrees":
        # return palettable.cartocolors.qualitative.Pastel_10.hex_colors
        return palettable.colorbrewer.qualitative.Set3_12.hex_colors
        # return palettable.matplotlib.Viridis_12.hex_colors
        # return palettable.tableau.PurpleGray_12.hex_colors
        # return sns.color_palette("muted", 12).as_hex()  # WARNING: this contains only 10 distinct colors!!!
    else:
        raise ValueError(f"Unexpected value: {unit.value}")


def plot_single_stacked_bar_for_relative_frequencies(
    values, *, ax, xpos, color_palette, width=0.6, sort_freqs_ascending=False
):
    """
    Parameters
    ----------
    values : pandas.Series
        The relative frequency values to plot (note that these must add up to 100.0)
    ax : AxesSubplot
        The matplotlib axes to which to add the stacked bar chart.
    xpos : float
        The x-position at which to add the stacked bar to the existing plot.
    color_palette : list
        List of hex color values to use.
    width : float
        Width of each bar.
    sort_freqs_ascending : bool
        If True, sort the relative frequency values in ascending order before assembling
        them into the stacked bar (default: False).
    """
    assert np.isclose(values.sum(), 100.0)  # ensure relative frequencies add up to 100%

    # # color_palette = palettable.colorbrewer.qualitative.Set2_8.hex_colors
    # # color_palette = palettable.cartocolors.qualitative.Pastel_8.hex_colors
    # color_palette = palettable.cartocolors.qualitative.Vivid_8.hex_colors
    # # color_palette = palettable.tableau.Tableau_10.hex_colors

    df_s = pd.DataFrame({"value": values, "color": color_palette[: len(values)]})
    if sort_freqs_ascending:
        df_s = df_s.sort_values("value", ascending=False)
    df_s["value_cum"] = df_s["value"].cumsum().shift(fill_value=0)
    for value, color, bottom in df_s.itertuples(index=False):
        ax.bar(xpos, value, bottom=bottom, width=width, color=color)


def plot_stacked_bar_chart_for_relative_pc_frequencies(
    dendrogram_nodes,
    *,
    cols_with_nonzero_entries,
    color_palette,
    ax=None,
    title=None,
    figsize=(20, 4),
    use_tight_layout=True,
    sort_freqs_ascending=False,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        plt.close(fig)
    else:
        fig = ax.figure

    num_clusters = len(dendrogram_nodes)
    for i, n in enumerate(dendrogram_nodes):
        # Note: since we're extracting the non-zero entries from n.distribution
        # we must also use the non-zero column names for the legend entries below!
        plot_single_stacked_bar_for_relative_frequencies(
            n.avg_distribution[cols_with_nonzero_entries],
            color_palette=color_palette,
            xpos=i,
            ax=ax,
            width=0.6,
            sort_freqs_ascending=sort_freqs_ascending,
        )
    ax.set_xticks(list(range(num_clusters + 1)))
    ax.set_xticklabels([f"Cluster {n.id}:\n{n.num_leaves} leaves" for n in dendrogram_nodes])

    if num_clusters > 0:
        legend_labels = [
            x.value for x in cols_with_nonzero_entries
        ]  # TODO: this relies on the assumption that the column labels are enums; would be good to encapsulate this better
        legend_elements = [
            Patch(facecolor=color, edgecolor=color, label=value)
            for value, color in reversed(list(zip(legend_labels, color_palette)))
        ]
        ax.legend(handles=legend_elements, loc="right")

    if title:
        ax.set_title(title)
    if use_tight_layout:
        fig.tight_layout()
    return fig
