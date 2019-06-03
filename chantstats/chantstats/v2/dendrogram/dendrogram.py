import matplotlib.pyplot as plt
import numpy as np
import palettable
import scipy.stats
from scipy.cluster.hierarchy import dendrogram, linkage, set_link_color_palette, to_tree
from scipy.spatial.distance import pdist
from ..analysis_functions import get_analysis_function
from ..analysis_type import AnalysisType
from ..logging import logger
from ..unit import UnitType
from ..utils import plot_empty_figure
from .dendrogram_node import DendrogramNode

__all__ = ["calculate_dendrogram"]


class EmptyDendrogramError(Exception):
    """
    Indicates an error in the dendrogram calculation due to an insufficient number of input nodes.
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
        raise EmptyDendrogramError("Cannot produce dendrogram for a single item (nothing to cluster).")
    Z = linkage(
        pdist(df_freq_distributions.values, metric=calculate_distribution_distance),
        method="complete",
        optimal_ordering=optimal_ordering,
    )
    return Z


class Dendrogram:
    def __init__(self, df, *, analysis, optimal_ordering=True):
        if df.isnull().any(axis=None):
            raise RuntimeError(
                "Dataframe contains NaN values. Please filter them out before calculating the dendrogram"
            )

        self.df_orig = df
        self.analysis = AnalysisType(analysis)
        cols_with_nonzero_entries = df.columns[(df != 0).any()]
        if sorted(cols_with_nonzero_entries) != sorted(df.columns):
            missing_columns = sorted([x for x in set(df.columns).difference(cols_with_nonzero_entries)])
            logger.debug(f"Removed zero-valued columns from dataframe: {missing_columns}")

        self.df = df[cols_with_nonzero_entries]
        if any((df == 0).all(axis=1)):
            logger.warning(
                "Dataframe contains rows with all-zero entries (which previously may have been all-NaN values). "
                "Currently these are dropped as part of the dendrogram calculation!"
            )
            logger.warning(
                "The following rows have been dropped: " + ", ".join(self.df[(self.df == 0).all(axis=1)].index)
            )
            self.df = self.df[(self.df != 0).any(axis=1)]

        self.L = calculate_linkage_matrix_in_python_format(self.df, optimal_ordering=optimal_ordering)
        self.R = dendrogram(self.L, no_plot=True)
        self.root_node, self.all_cluster_nodes = to_tree(self.L, rd=True)
        self.leaf_ids = self.root_node.pre_order(lambda x: x.id)
        self.all_cluster_nodes = [
            DendrogramNode(
                df,
                cn,
                analysis=self.analysis,
                all_leaf_ids=self.leaf_ids,
                cols_with_globally_nonzero_entries=cols_with_nonzero_entries,
            )
            for cn in self.all_cluster_nodes
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

    def get_nodes_below_cutoff(self, p_cutoff, *, include_leaf_nodes):
        proper_cluster_condition = lambda node: True if include_leaf_nodes else not node.is_leaf

        return sorted(
            [
                n
                for n in self.all_cluster_nodes
                if proper_cluster_condition(n)
                and n.dist < p_cutoff
                and (n.parent is None or (n.parent is not None and n.parent.dist > p_cutoff))
            ],
            key=lambda n: n.num_leaves,
            reverse=True,
        )

    def get_cluster_node(self, cluster_id):
        cluste_node = self.all_cluster_nodes[cluster_id]
        assert cluste_node.id == cluster_id
        return cluste_node

    def plot_dendrogram(
        self,
        p_cutoff,
        *,
        result_descriptor=None,
        ax=None,
        title=None,
        figsize=(22, 4),
        ylim=(0.0, 1.0),
        leaf_font_size=10,
        annotate_nodes_below_cutoff=True,
        annotate_all_nodes=False,
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

        def get_leaf_id(label):
            leaf_nodes_with_label = [n for n in self.leaf_nodes if n.descr == label]
            if len(leaf_nodes_with_label) == 1:
                return f"#{leaf_nodes_with_label[0].id}: "
            else:
                # raise RuntimeError(
                #     f"Could not find leaf unique node with label '{label}'. Found: {leaf_nodes_with_label}"
                # )
                logger.error(f"Could not find leaf unique node with label '{label}'. Found: {leaf_nodes_with_label}")
                return ""

        xticklabels = [f"{get_leaf_id(label)}{label}" for label in self.df.index]

        R = dendrogram(
            self.L,
            labels=xticklabels,
            truncate_mode=None,
            color_threshold=p_cutoff,
            above_threshold_color="#999999",
            leaf_rotation=90.0,  # rotates the x axis labels
            leaf_font_size=leaf_font_size,  # font size for the x axis labels
            ax=ax,
        )
        set_link_color_palette(None)  # reset to default

        # Calculate the "proper" clusters (containing at least two leaf nodes) below p_cutoff
        nodes_below_cutoff = self.get_nodes_below_cutoff(p_cutoff, include_leaf_nodes=False)
        size_nodes_below_cutoff = 20
        size_other_nodes = 10

        # Add horizontal line at p_cutoff
        ax.axhline(y=p_cutoff, linewidth=0.5, linestyle=":", color="gray")

        # Draw dots to indicate the dendrogram nodes which are not leaves
        for n in self.all_cluster_nodes:
            if not n.is_leaf and not n in nodes_below_cutoff:
                ax.scatter(n.xpos, n.ypos, s=size_other_nodes, zorder=2, color="gray")

        if annotate_all_nodes:
            annotate_nodes_below_cutoff = False  # avoid double annotations below

        if annotate_nodes_below_cutoff:
            for i, n in enumerate(nodes_below_cutoff):
                ax.annotate(n.id, xy=(n.xpos, n.ypos), xycoords="data", xytext=(4, 4), textcoords="offset points")
                ax.scatter(n.xpos, n.ypos, s=size_nodes_below_cutoff, zorder=2, color="gray")

        if annotate_all_nodes:
            for i, n in enumerate(self.all_cluster_nodes):
                ax.annotate(n.id, xy=(n.xpos, n.ypos), xycoords="data", xytext=(4, 4), textcoords="offset points")
                ax.scatter(n.xpos, n.ypos, s=size_nodes_below_cutoff, zorder=2, color="gray")

        ax.set_ylim(ylim)
        ax.axhline(y=0.0, linewidth=0.5, color="black")

        if title is None and result_descriptor is not None:
            title = result_descriptor.plot_title
        if title:
            ax.set_title(title)
        if use_tight_layout:
            fig.tight_layout()
        return fig


class EmptyDendrogram:
    """
    Stub class representing an empty dendrogram (with just enough functionality
    so that code which interacts with regular dendrograms still works).
    """

    def __init__(self, df, *, analysis):
        self.df_orig = df
        self.df_trimmed = df[(df != 0).any(axis=1)]
        self.analysis = AnalysisType(analysis)
        if len(self.df_trimmed) > 1:
            raise RuntimeError(
                f"Unexpected size of trimmed input data frame: {len(self.df_trimmed)}.\n\n{self.df_trimmed}"
            )
        else:
            if len(self.df_orig) > 1:
                logger.warning(
                    f"Plotting empty dendrogram because input dataframe (with {len(self.df_orig)} rows) "
                    "contains a row with only zero values."
                )

    def plot_dendrogram(self, p_cutoff, *, result_descriptor=None, figsize=(22, 4)):
        # msg_text = "This dendrogram plot is deliberately empty\nbecause there is only a single input item."
        msg_text = "This dendrogram plot is deliberately empty\nbecause there is nothing to cluster."
        fig = plot_empty_figure(msg_text, result_descriptor=result_descriptor, figsize=figsize)
        return fig

    def get_nodes_below_cutoff(self, p_cutoff, *, include_leaf_nodes):
        return []


def calculate_dendrogram(modal_category, *, analysis, unit, analysis_func=None, replace_nan_values_with_zeros=True):
    unit = UnitType(unit)
    analysis = AnalysisType(analysis)
    analysis_func = analysis_func or get_analysis_function(analysis)

    df = modal_category.make_results_dataframe(analysis_func=analysis_func, unit=unit)
    if replace_nan_values_with_zeros:
        if df.isnull().values.any():
            logger.warning("Replacing NaN values with zeros in dendrogram dataframe.")
        # df = df[df.notna().all(axis=0)]  # drop any columns with
        df = df.fillna(0)

    try:
        dendrogram = Dendrogram(df, analysis=analysis)
    except EmptyDendrogramError:
        dendrogram = EmptyDendrogram(df, analysis=analysis)

    return dendrogram
