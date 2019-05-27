from scipy.cluster.hierarchy import ClusterNode
from ..logging import logger

__all__ = ["DendrogramNode"]


class DendrogramNode:
    def __init__(self, df_full, cluster_node, *, analysis, all_leaf_ids, cols_with_globally_nonzero_entries):
        assert isinstance(cluster_node, ClusterNode)
        self.analysis = analysis  # self.analysis = AnalysisType(analysis)
        self.df_full = df_full
        self.cols_with_globally_nonzero_entries = cols_with_globally_nonzero_entries
        self.cluster_node = cluster_node
        self.id = self.cluster_node.get_id()
        self.cluster_id = (
            # FIXME: this is currently the same as the internal id, but it should be a more intuitive number
            # (e.g. starting at 1 for the cluster with the most leaf nodes)
            self.id
        )
        self.dist = self.cluster_node.dist
        self.ypos = self.dist  # alias
        self.is_leaf = self.cluster_node.is_leaf()
        self.num_leaves = self.cluster_node.get_count()
        self.leaf_ids = self.cluster_node.pre_order(lambda x: x.id)
        self.df_cluster = self.df_full.iloc[self.leaf_ids]  # dataframe containig only the leaves in this cluster
        self.df_cluster_without_zero_rows = self.df_cluster[(self.df_cluster != 0).any(axis=1)]
        self.avg_distribution = self.df_cluster_without_zero_rows.mean()  #  average distribution of all leaf nodes

        if self.is_leaf:
            self.descr = self.df_full.index[self.id]
        else:
            self.descr = f"Cluster #{self.id}\n({self.num_leaves} leaves)"

        if len(self.df_cluster_without_zero_rows) < len(self.df_cluster):
            logger.warning(f"DendrogramNode dataframe contains zero rows: {self}")

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
        leaf_info = f" (leaf node: '{self.descr}')" if self.is_leaf else f" ({self.num_leaves} leaves: {self.leaf_ids})"
        return f"<DendrogramNode: id={self.id}{leaf_info}>"

    def plot_leaf_distributions(self, figsize=(8, 4)):
        """
        Plot distributions of the leaf nodes in this cluster as a multiple bar plot.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        ax = self.df_cluster.T.plot.bar(figsize=figsize)
        ax.set_xticklabels([x.str_value for x in self.df_cluster.columns], rotation=0)
        ax.set_title(f"Cluster #{self.id} ({self.num_leaves} leaves, p={self.dist:.2f})")
        ax.set_xlabel(self.df_cluster.columns[0].get_class_description())
        ax.set_ylabel("Rel. frequency (%)")  # TODO: this may not always be relative frequencies!
        ax.set_ylim(0, 105)
        ax.grid()
        fig = ax.figure
        plt.close(fig)
        return fig
