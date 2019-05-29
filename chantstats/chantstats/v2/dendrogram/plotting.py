import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
from ..utils import is_close_to_zero_or_100

__all__ = ["plot_pc_freq_distributions", "plot_tendency_distributions"]


def prepare_axes_for_stacked_bar_chart(ax, num_bars):
    ax.clear()
    ax.set_xticks(range(num_bars))
    ax.set_xlim(-0.5, num_bars + 0.5)
    ax.set_ylim(0.0, 105.0)  # y-axis contains percentages between 0% and 100%


def add_color_palette_legend(ax, *, labels, color_palette):
    legend_elements = [
        Patch(facecolor=color, edgecolor=color, label=value)
        for value, color in reversed(list(zip(labels, color_palette)))
    ]
    ax.legend(handles=legend_elements, loc="right")


def plot_single_pandas_series_as_stacked_bar(values, *, ax, xpos, color_palette, bar_width, sort_freqs_ascending=True):
    """
    Plot pandas series as a single stacked bar (as part of a full stacked bar chart).

    Parameters
    ----------
    values : pandas.Series
        The values to plot. Note that these must add up to 100.0 (because they represent relative frequency values).
    ax : AxesSubplot
        The matplotlib axes to which to add the stacked bar chart.
    xpos : float
        The x-position at which to draw the stacked bar to the axes.
    color_palette : list
        List of hex color values to use.
    bar_width : float
        Width of the bar.
    sort_freqs_ascending : bool
        If True, sort the relative frequency values in ascending order before assembling
        them into the stacked bar (default: True).
    """
    assert isinstance(values, pd.Series)
    assert not isinstance(values.index, pd.MultiIndex)
    # assert np.isclose(values.sum(), 100.0)
    if not is_close_to_zero_or_100(values.sum()):
        raise RuntimeError(f"Expected values close to 0 or 100 but they sum up to {values.sum()}. Values: {values}")

    colors = color_palette[: len(values)]
    if len(colors) < len(values):
        raise RuntimeError(
            f"Color palette does not contain enough colors (contains {len(colors)}, needs {len(values)})"
        )
    df_s = pd.DataFrame({"value": values, "color": colors})
    if sort_freqs_ascending:
        df_s = df_s.sort_values("value", ascending=False)
    df_s["value_cum"] = df_s["value"].cumsum().shift(fill_value=0)
    for value, color, bar_bottom in df_s.itertuples(index=False):
        ax.bar(xpos, value, bottom=bar_bottom, width=bar_width, color=color)
        if value >= 4.0:
            xy_text = (xpos, bar_bottom + 0.5 * value)
            horizontalalignment = "center"
            # xy_text = (xpos + 0.5 * bar_width, bar_bottom + 0.5 * value)
            # horizontalalignment = "left"
            ax.annotate(f"{value:.1f}", xy=xy_text, horizontalalignment=horizontalalignment, verticalalignment="center")


def plot_multiple_pandas_series_as_stacked_bar_chart(
    series, *, xlabels, ax, color_palette, title, bar_width, sort_freqs_ascending=True
):
    """
    Plot a collection of pandas series as a stacked bar chart (with one stacked bar per series).

    Parameters
    ----------
    series : list of pandas.Series
        The values to plot. Note that each of these must add up to 100.0 (because they represent relative frequency values).
    xlabels : list of str
        The x-axis labels for the resulting stacked bars.
    ax : AxesSubplot
        The matplotlib axes to which to add the stacked bar chart.
    color_palette : list
        List of hex color values to use.
    bar_width : float
        Width of the bar.
    sort_freqs_ascending : bool
        If True, sort the relative frequency values in ascending order before assembling
        them into the stacked bar (default: True).
    """
    prepare_axes_for_stacked_bar_chart(ax, num_bars=len(series))

    # Plot stacked bars and associated x-axis labels
    for idx, s in enumerate(series):
        plot_single_pandas_series_as_stacked_bar(
            s,
            ax=ax,
            xpos=idx,
            color_palette=color_palette,
            bar_width=bar_width,
            sort_freqs_ascending=sort_freqs_ascending,
        )
    ax.set_xticklabels(xlabels)

    # Add legend
    assert len(set([tuple(s.index) for s in series])) == 1  # ensure all series objects share the same index
    legend_labels = [
        x.label_for_plots for x in series[0].index
    ]  # TODO: this relies on the fact that the index values are enums; would be good to make this more explicit
    add_color_palette_legend(ax, labels=legend_labels, color_palette=color_palette)

    # Add plot title
    ax.set_title(title)

    return ax


def plot_pc_freq_distributions(
    dendrogram_nodes, *, result_descriptor, color_palette, bar_width=0.6, sort_freqs_ascending=True, figsize=(20, 4)
):
    """
    Create a stacked bar chart from the PC frequency distributions of the given dendrogram nodes.
    """

    def make_xlabel_for_cluster_node(node):
        if node.num_leaves > 1:
            return f"#{node.cluster_id}\n({node.num_leaves} leaves)"
        else:
            return f"Leaf node:\n{node.descr}"

    series = [n.avg_distribution for n in dendrogram_nodes]
    xlabels = [make_xlabel_for_cluster_node(n) for n in dendrogram_nodes]
    title = result_descriptor.plot_title

    fig, ax = plt.subplots(figsize=figsize)
    plot_multiple_pandas_series_as_stacked_bar_chart(
        series,
        xlabels=xlabels,
        ax=ax,
        color_palette=color_palette,
        title=title,
        bar_width=bar_width,
        sort_freqs_ascending=sort_freqs_ascending,
    )
    ax.set_xlabel("Clusters", labelpad=15)
    ax.set_ylabel("Probability of occurrence (in percent)", rotation="vertical")
    plt.close(fig)

    return fig


# TODO: can we use exactly the same function here?!?
plot_LMO_freq_distributions = plot_pc_freq_distributions


def plot_tendency_distributions(
    dendrogram_node,
    *,
    result_descriptor,
    color_palette,
    ax=None,
    bar_width=0.6,
    sort_freqs_ascending=True,
    figsize=(20, 4),
):
    """
    Create a stacked bar chart from the PC tendency distributions of the given dendrogram node.
    """
    fig, ax = plt.subplots(figsize=figsize) if ax is None else (ax.figure, ax)

    # df = dendrogram_node.distribution.values
    df = dendrogram_node.avg_distribution.unstack(level=0)
    series = [df[col] for col in df.columns]
    title = result_descriptor.plot_title
    xlabels = [pc.label_for_plots for pc in df.columns]

    plot_multiple_pandas_series_as_stacked_bar_chart(
        series,
        xlabels=xlabels,
        ax=ax,
        color_palette=color_palette,
        title=title,
        bar_width=bar_width,
        sort_freqs_ascending=sort_freqs_ascending,
    )
    ax.set_ylabel("Probability of occurrence (in percent)", rotation="vertical")
    return fig
