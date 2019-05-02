import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import palettable
from matplotlib.patches import Patch
from scipy.cluster.hierarchy import dendrogram, set_link_color_palette, to_tree, ClusterNode

from .dendrogram import calculate_linkage_matrix_in_python_format


def plot_stacked_bar_chart_for_relative_frequencies(
    s, *, xpos, ax, color_palette, width=0.6, sort_freqs_ascending=False
):
    assert np.isclose(s.sum(), 100.0)  # ensure relative frequencies add up to 100%

    # # color_palette = palettable.colorbrewer.qualitative.Set2_8.hex_colors
    # # color_palette = palettable.cartocolors.qualitative.Pastel_8.hex_colors
    # color_palette = palettable.cartocolors.qualitative.Vivid_8.hex_colors
    # # color_palette = palettable.tableau.Tableau_10.hex_colors

    df_s = pd.DataFrame({"value": s, "color": color_palette[: len(s)]})
    if sort_freqs_ascending:
        df_s = df_s.sort_values("value", ascending=False)
    df_s["value_cum"] = df_s["value"].cumsum().shift(fill_value=0)
    for value, color, bottom in df_s.itertuples(index=False):
        ax.bar(xpos, value, bottom=bottom, width=width, color=color)


class DendrogramNode:
    def __init__(self, df_full, cluster_node, *, all_leaf_ids):
        assert isinstance(cluster_node, ClusterNode)
        self.df_full = df_full
        self.cluster_node = cluster_node
        self.id = self.cluster_node.get_id()
        self.dist = self.cluster_node.dist
        self.ypos = self.dist  # alias
        self.is_leaf = self.cluster_node.is_leaf()
        self.num_leaves = self.cluster_node.get_count()
        self.leaf_ids = self.cluster_node.pre_order(lambda x: x.id)
        self.avg_distribution = self.df_full.iloc[self.leaf_ids].mean()  #  average distribution of all leaf nodes

        # The following are helpful for plotting because they determine
        # the left/right edge of the cluster.
        self.leftmost_idx = all_leaf_ids.index(self.leaf_ids[0])
        self.rightmost_idx = all_leaf_ids.index(self.leaf_ids[-1])
        self.xpos_left_boundary = self.leftmost_idx * 10.0
        self.xpos_right_boundary = (self.rightmost_idx + 1) * 10.0

    @property
    def xpos(self):
        if self.is_leaf:
            assert self.leftmost_idx == self.rightmost_idx
            return 5.0 + self.leftmost_idx * 10.0
        else:
            return 0.5 * (self.left.xpos + self.right.xpos)

    def __repr__(self):
        leaf_info = " (leaf node)" if self.is_leaf else f" ({self.num_leaves} leaves: {self.leaf_ids})"
        return f"<DendrogramNode: id={self.id}{leaf_info}>"


class Dendrogram:
    def __init__(self, df, *, p_threshold=0.15, optimal_ordering=True):
        self.df_orig = df
        self.cols_with_nonzero_entries = df.columns[(df != 0).any()]
        self.df = self.df_orig[self.cols_with_nonzero_entries]
        self.L = calculate_linkage_matrix_in_python_format(df, optimal_ordering=optimal_ordering)
        self.p_threshold = p_threshold
        self.R = dendrogram(self.L, no_plot=True)
        root_node, all_cluster_nodes = to_tree(self.L, rd=True)
        self.leaf_ids = root_node.pre_order(lambda x: x.id)
        self.all_cluster_nodes = [DendrogramNode(df, cn, all_leaf_ids=self.leaf_ids) for cn in all_cluster_nodes]
        self.root_node = [n for n in self.all_cluster_nodes if n.cluster_node is root_node][0]  # TODO: simplify this

        # Retroactively assign left/right children to each DendrogramNode
        for n in self.all_cluster_nodes:
            if not n.is_leaf:
                n.left = self.all_cluster_nodes[n.cluster_node.left.id]
                n.right = self.all_cluster_nodes[n.cluster_node.right.id]
                n.left.parent = n
                n.right.parent = n
        self.root_node.parent = None

        self.nodes_below_cutoff = sorted(
            [
                n
                for n in self.all_cluster_nodes
                if not n.is_leaf
                and n.dist < self.p_threshold
                and n.parent is not None
                and n.parent.dist > self.p_threshold
            ],
            key=lambda n: n.num_leaves,
            reverse=True,
        )

    def plot_dendrogram(
        self,
        *,
        ax=None,
        title=None,
        figsize=(20, 4),
        leaf_font_size=10,
        annotate_nodes_below_cutoff=True,
        link_color_palette=None,
        use_tight_layout=True,
    ):
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
            plt.close(fig)
        else:
            fig = ax.figure

        link_color_palette = link_color_palette or palettable.tableau.Tableau_10.hex_colors
        set_link_color_palette(link_color_palette)
        R = dendrogram(
            self.L,
            labels=self.df.index,
            truncate_mode=None,
            color_threshold=self.p_threshold,
            above_threshold_color="#999999",
            leaf_rotation=90.0,  # rotates the x axis labels
            leaf_font_size=leaf_font_size,  # font size for the x axis labels
            ax=ax,
        )
        set_link_color_palette(None)  # reset to default

        if annotate_nodes_below_cutoff:
            for i, n in enumerate(self.nodes_below_cutoff):
                ax.annotate(n.id, xy=(n.xpos, n.ypos), xycoords="data", xytext=(4, 4), textcoords="offset points")
                ax.scatter(n.xpos, n.ypos, zorder=2, color="gray")
        if title:
            ax.set_title(title)
        if use_tight_layout:
            fig.tight_layout()
        return fig

    def plot_stacked_bar_charts(
        self, *, color_palette, ax=None, title=None, figsize=(20, 4), use_tight_layout=True, sort_freqs_ascending=False
    ):
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
            plt.close(fig)
        else:
            fig = ax.figure

        num_clusters = len(self.nodes_below_cutoff)
        for i, n in enumerate(self.nodes_below_cutoff):
            # Note: since we're extracting the non-zero entries from n.distribution
            # we must also use the non-zero column names for the legend entries below!
            plot_stacked_bar_chart_for_relative_frequencies(
                n.avg_distribution[self.cols_with_nonzero_entries],
                color_palette=color_palette,
                xpos=i,
                ax=ax,
                width=0.6,
                sort_freqs_ascending=sort_freqs_ascending,
            )
        ax.set_xticks(list(range(num_clusters + 1)))
        ax.set_xticklabels([f"Cluster {n.id}:\n{n.num_leaves} leaves" for n in self.nodes_below_cutoff])

        if num_clusters > 0:
            legend_labels = self.cols_with_nonzero_entries
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
