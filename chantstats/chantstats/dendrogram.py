import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist

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


def plot_dendrogram(df_freq_distributions, *, p_threshold=0.15, figsize=(16, 5), leaf_font_size=10):
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

    Returns
    -------
    matplotlib.figure.Figure
        Matplotlib figure containing the dendrogram plot.
    """
    assert isinstance(df_freq_distributions, pd.DataFrame)
    Z = linkage(pdist(df_freq_distributions.values, metric=calculate_distribution_distance), method="complete")
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
