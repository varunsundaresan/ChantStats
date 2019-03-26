import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy.stats
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist

from .logging import logger

__all__ = ["plot_dendrogram"]


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


class DendrogramError(Exception):
    """
    Indicates an error in the dendrogram calculation.
    """


def calculate_linkage_matrix_in_python_format(df_freq_distributions, *, optimal_ordering=True):
    if len(df_freq_distributions) <= 1:
        raise DendrogramError("Cannot produce dendrogram for a single item (nothing to cluster).")
    Z = linkage(
        pdist(df_freq_distributions.values, metric=calculate_distribution_distance),
        method="complete",
        optimal_ordering=optimal_ordering,
    )
    return Z


def plot_dendrogram(
    df_freq_distributions, *, p_threshold=0.15, figsize=(16, 5), leaf_font_size=10, optimal_ordering=True
):
    """
    Plot a dendrogram

    Parameters
    ----------
    df_freq_distributions : pandas.DataFrame
        Data frame containing the frequency distributions for which to calculate the dendrogram.
        Must contain one frequency distribution per row. The row labels will be used as the
        labels for the dendrogram leaf nodes.
    p_threshold : float
        Value of p which is considered the threshold for distributions to be considered "similar".
        All links above this threshold will be colored gray.
    figsize : pair of float
        Size of the output figure (in inches). Same as matplotlib figsize.
    leaf_font_size : int
        Font size to use for the labels of leaf notes.
    optimal_ordering : bool
        If True, the linkage matrix will be reordered so that the distance between successive leaves
        is minimal. This results in a more intuitive tree structure when the data are visualized.
        Note that this algorithm can be slow, particularly on large datasets. See the function
        `scipy.cluster.hierarchy.linkage` for details.

    Returns
    -------
    matplotlib.figure.Figure
        Matplotlib figure containing the dendrogram plot.
    """
    assert isinstance(df_freq_distributions, pd.DataFrame)
    Z = calculate_linkage_matrix_in_python_format(df_freq_distributions, optimal_ordering=optimal_ordering)
    labels = df_freq_distributions.index
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title("Hierarchical Clustering Dendrogram")
    # ax.set_xlabel('Pieces')
    ax.set_ylabel("Height")
    dendrogram(
        Z,
        labels=labels,
        truncate_mode=None,
        color_threshold=p_threshold,
        above_threshold_color="#999999",
        leaf_rotation=90.0,  # rotates the x axis labels
        leaf_font_size=leaf_font_size,  # font size for the x axis labels
        ax=ax,
    )
    ax.axhline(y=p_threshold, c="grey", lw=1, linestyle="dashed")
    ax.set_ylim(-0.05, 1.05)
    fig.tight_layout()
    plt.close(fig)
    return fig


class DendrogramNode:
    def __init__(self, *, descr, index, p_coeff, y_pos, payload, children):
        self.index = index
        self.p_coeff = p_coeff
        self.y_pos = y_pos
        self.payload = payload
        self.children = children
        self.parent = None

        self.is_leaf = self.children == []
        self.num_leaves = 1 if self.is_leaf else sum([c.num_leaves for c in self.children])
        self.num_descendants = sum([c.num_descendants for c in self.children]) + 1
        self.descr = descr or "Cluster with {} leaves".format(self.num_leaves)

        if payload is not None:
            assert isinstance(payload, pd.Series)
            self.payload = payload  # TODO: if payload==None, set this to the averaged distribution of all leaves
        else:
            # Set payload to the average of the leaf payloads
            leaf_payloads = [c.payload for c in self.leaves]
            zero_payload = pd.Series(0, index=leaf_payloads[0].index)
            self.payload = sum(leaf_payloads, zero_payload) / len(leaf_payloads)

        self.df = pd.DataFrame([n.payload for n in self.leaves])

    def __repr__(self):
        if self.is_leaf:
            descr_descendants = "leaf node"
        else:
            descr_descendants = (
                f"{self.num_descendants} descendants, "
                f"{self.num_leaves} leaves, "
                f"immediate children: {[c.index for c in self.children]}"
            )
        return f"<DendrogramNode: '{self.descr}', idx: {self.index} ({descr_descendants})>"

    @property
    def descendants(self):
        yield self
        for c in self.children:
            yield from c.descendants

    @property
    def leaves(self):
        for n in self.descendants:
            if n.is_leaf:
                yield n

    @property
    def left_child(self):
        try:
            return self.children[0]
        except IndexError:
            raise DendrogramError("Leaf node does not have any children.")

    @property
    def right_child(self):
        try:
            return self.children[1]
        except IndexError:
            raise DendrogramError("Leaf node does not have any children.")

    def get_max_nodes_below_cutoff(self, p_cutoff, *, exclude_leaf_nodes=True):
        if p_cutoff >= 1.0:
            raise ValueError("The value of p_cutoff must be less than 1.0")

        max_nodes = [n for n in self.descendants if n.p_coeff <= p_cutoff and n.parent.p_coeff > p_cutoff]
        if exclude_leaf_nodes:
            max_nodes = [n for n in max_nodes if not n.is_leaf]
        return max_nodes


def make_dendrogram_tree(df):
    """
    Create a dendrogram tree from frequency distributions.

    Parameters
    ----------
    df : pandas.DataFrame
        The input data frame. Must contain one row per distribution.

    Returns
    -------
    DendrogramNode
        The root node of the dendrogram.
    """
    ZZZ = calculate_linkage_matrix_in_python_format(df)

    # set idx to the index of the root node (= the one with the largest number of descendants)
    root_node_idx = int(ZZZ[:, 3].argmax())

    N = len(df)
    return make_dendrogram_subtree(df, root_node_idx + N, ZZZ, N)


def make_dendrogram_subtree(df, idx, ZZZ, N):

    if idx < N:
        # leaf node
        result = DendrogramNode(
            descr=str(df.index[idx]), index=idx, p_coeff=0, y_pos=100.0, payload=df.iloc[idx], children=[]
        )
    else:
        i = int(ZZZ[idx - N, 0])
        j = int(ZZZ[idx - N, 1])
        p_coeff = ZZZ[idx - N, 2]
        left_child = make_dendrogram_subtree(df, i, ZZZ, N)
        right_child = make_dendrogram_subtree(df, j, ZZZ, N)
        children = [left_child, right_child]
        result = DendrogramNode(
            descr=None, index=idx, p_coeff=p_coeff, y_pos=(100 * (1 - p_coeff)), payload=None, children=children
        )
        left_child.parent = result
        right_child.parent = result

    return result


def plot_bar_chart_for_dendrogram_node_payload(node, ymax=None, figsize=(8, 4)):
    """
    Plot a bar chart based on the payload of the given dendrogram node.

    Parameters
    ----------
    node : DendrogramNode
        The dendrogram node of which to plot the payload.
    ymax : float, optional
        Set the y-axis limit of the bar chart to this value (optional).
    figsize : (float, float), optional
        Width and height of the resulting figure in inches.

    Returns
    -------
    matplotlib.figure.Figure
    """
    assert isinstance(node, DendrogramNode)
    fig, ax = plt.subplots(figsize=figsize)
    node.payload.plot.bar(ax=ax)
    title = f"DendrogramNode with {len(list(node.leaves))} leaves (index: {node.index})"
    ax.set_title(title)
    ax.set_ylim(0, ymax)
    plt.close(fig)
    return fig


def export_max_nodes_below_cutoff(tree, *, output_dir, p_cutoff, ymax=None, fmt="pdf"):
    """
    Given a dendrogram tree, find the "maximal" nodes whose p-value
    is below `p_cutoff` and export a bar chart for each of these nodes'
    distributions in the directory `output_dir`.
    """
    assert isinstance(tree, DendrogramNode)

    supported_output_formats = ["pdf", "png"]
    if fmt not in supported_output_formats:
        raise ValueError(f"Unsupported output format: '{fmt}'. Supported formats are: {supported_output_formats}")

    ymax = ymax or tree.df.max().max()

    logger.debug(f"Exporting bar charts to directory: '{output_dir}'")
    os.makedirs(output_dir, exist_ok=True)
    nodes = tree.get_max_nodes_below_cutoff(p_cutoff=p_cutoff)
    for node in nodes:
        fig = plot_bar_chart_for_dendrogram_node_payload(node, ymax=ymax)
        outfilename = f"bar_chart_for_dendrogram_node_{node.index:03d}.{fmt}"
        logger.debug(f"Saving bar chart to file: '{outfilename}'")
        output_path = os.path.join(output_dir, outfilename)
        fig.savefig(output_path)
