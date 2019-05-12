import matplotlib.pyplot as plt

from .dendrogram2 import plot_stacked_bar_chart_for_relative_frequencies


def prepare_figure_for_pc_freqs_plot(dendrogram_nodes_below_p_cutoff, figsize=(20, 4)):
    fig, ax = plt.subplots(figsize=figsize)

    num_clusters = len(dendrogram_nodes_below_p_cutoff)
    ax.set_xticks(list(range(num_clusters + 1)))
    ax.set_xticklabels([n.descr for n in dendrogram_nodes_below_p_cutoff])

    ax.set_xlim(-0.5, num_clusters - 0.5)
    ax.set_ylim(-10, 110)

    plt.close(fig)

    return fig, ax


def create_plot_for_pc_freqs(dendrogram, color_palette, bar_width=0.6, figsize=(20, 4)):
    fig, ax = prepare_figure_for_pc_freqs_plot(dendrogram.nodes_below_p_cutoff, figsize=figsize)
    for idx, n in enumerate(dendrogram.nodes_below_p_cutoff):
        plot_stacked_bar_chart_for_relative_frequencies(
            n.distribution, xpos=idx, ax=ax, color_palette=color_palette, width=bar_width, sort_freqs_ascending=False
        )

    #     # Add labels for stacked bars (here: PC names)
    #     s = df.iloc[idx]
    #     labels_ypos = s.cumsum().shift(fill_value=0) + 0.5 * s
    #     for label, ypos in labels_ypos.iteritems():
    #         ax.text(idx + 0.55 * width, ypos, label, verticalalignment="center")

    return fig, ax
