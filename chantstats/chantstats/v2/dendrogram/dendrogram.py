import matplotlib.pyplot as plt
import numpy as np
import palettable
import scipy.stats
from scipy.cluster.hierarchy import dendrogram, linkage, set_link_color_palette, to_tree
from scipy.spatial.distance import pdist
from ..analysis_functions import get_analysis_function, AnalysisType
from ..logging import logger
from ..unit import UnitType
from .dendrogram_node import DendrogramNode

__all__ = ["calculate_dendrogram"]


class DendrogramError(Exception):
    """
    Indicates an error in the dendrogram calculation.
    """


def calculate_chi_square_p_value(A):
    """
    Calulate the p-value of the Pearson chi-square test when applied
    to the rows of the matrix A (interpreted as individual observations)

    Note: any values where both freqs1 and freqs2 are zero are discarded
    before calculating the chi-square value.
    """
    nonzero_columns = np.where(A.any(axis=0))[0]
    A_nonzero_columns = A[:, nonzero_columns]
    _, p_value, _, _ = scipy.stats.chi2_contingency(A_nonzero_columns)
    return p_value


def calculate_distribution_distance(freqs1, freqs2):
    """
    Calulate the "distance" between two frequency distributions.
    This is (1-p), where p is the p-value of the chi-square calculation
    returned by the function `calculate_chi_square_p_value`.
    """
    A = np.array([freqs1, freqs2])
    p_value = calculate_chi_square_p_value(A)
    return 1 - p_value


def calculate_linkage_matrix_in_python_format(df_freq_distributions, *, optimal_ordering=True):
    if len(df_freq_distributions) <= 1:
        raise DendrogramError("Cannot produce dendrogram for a single item (nothing to cluster).")
    Z = linkage(
        pdist(df_freq_distributions.values, metric=calculate_distribution_distance),
        method="complete",
        optimal_ordering=optimal_ordering,
    )
    return Z


class Dendrogram:
    def __init__(self, df, *, analysis, optimal_ordering=True):
        self.df_orig = df
        self.analysis = AnalysisType(analysis)
        self.cols_with_nonzero_entries = df.columns[(df != 0).any()]
        if sorted(self.cols_with_nonzero_entries) != sorted(df.columns):
            missing_columns = sorted([x.value for x in set(df.columns).difference(self.cols_with_nonzero_entries)])
            logger.debug(f"Removed zero-values columns from dataframe: {missing_columns}")
        self.df = self.df_orig[self.cols_with_nonzero_entries]
        self.L = calculate_linkage_matrix_in_python_format(df, optimal_ordering=optimal_ordering)
        self.R = dendrogram(self.L, no_plot=True)
        self.root_node, self.all_cluster_nodes = to_tree(self.L, rd=True)
        self.leaf_ids = self.root_node.pre_order(lambda x: x.id)
        self.all_cluster_nodes = [
            DendrogramNode(df, cn, analysis=self.analysis, all_leaf_ids=self.leaf_ids) for cn in self.all_cluster_nodes
        ]
        self.leaf_nodes = [n for n in self.all_cluster_nodes if n.is_leaf]
        self.root_node = [n for n in self.all_cluster_nodes if n.cluster_node is self.root_node][
            0
        ]  # TODO: simplify this

        # Retroactively assign left/right children to each DendrogramNode
        for n in self.all_cluster_nodes:
            if not n.is_leaf:
                n.left = self.all_cluster_nodes[n.cluster_node.left.id]
                n.right = self.all_cluster_nodes[n.cluster_node.right.id]
                n.left.parent = n
                n.right.parent = n
        self.root_node.parent = None

    def get_nodes_below_cutoff(self, p_cutoff):
        return sorted(
            [
                n
                for n in self.all_cluster_nodes
                if not n.is_leaf
                and n.dist < p_cutoff
                and (n.parent is None or (n.parent is not None and n.parent.dist > p_cutoff))
            ],
            key=lambda n: n.num_leaves,
            reverse=True,
        )

    def plot_dendrogram(
        self,
        p_cutoff,
        *,
        ax=None,
        title=None,
        figsize=(20, 4),
        ylim=(0.0, 1.0),
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
            color_threshold=p_cutoff,
            above_threshold_color="#999999",
            leaf_rotation=90.0,  # rotates the x axis labels
            leaf_font_size=leaf_font_size,  # font size for the x axis labels
            ax=ax,
        )
        set_link_color_palette(None)  # reset to default

        nodes_below_cutoff = self.get_nodes_below_cutoff(p_cutoff)
        size_nodes_below_cutoff = 20
        size_other_nodes = 10

        # Draw dots to indicate the dendrogram nodes which are not leaves
        for n in self.all_cluster_nodes:
            if not n.is_leaf and not n in nodes_below_cutoff:
                ax.scatter(n.xpos, n.ypos, s=size_other_nodes, zorder=2, color="gray")

        if annotate_nodes_below_cutoff:
            for i, n in enumerate(nodes_below_cutoff):
                ax.annotate(n.id, xy=(n.xpos, n.ypos), xycoords="data", xytext=(4, 4), textcoords="offset points")
                ax.scatter(n.xpos, n.ypos, s=size_nodes_below_cutoff, zorder=2, color="gray")

        ax.set_ylim(ylim)
        ax.axhline(y=0.0, linewidth=0.5, color="black")

        if title:
            ax.set_title(title)
        if use_tight_layout:
            fig.tight_layout()
        return fig


def calculate_dendrogram(modal_category, *, analysis, unit):
    unit = UnitType(unit)
    analysis = AnalysisType(analysis)
    analysis_func = get_analysis_function(analysis)
    df = modal_category.make_results_dataframe(analysis_func=analysis_func, unit=unit)
    # df = df[[col for col in df.columns[(df != 0).any()]]]  # remove columns where all values are zero
    dendrogram = Dendrogram(df, analysis=analysis)
    return dendrogram
