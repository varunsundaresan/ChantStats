from scipy.cluster.hierarchy import ClusterNode

__all__ = ["DendrogramNode"]


class DendrogramNode:
    def __init__(self, df_full, cluster_node, *, analysis_name, all_leaf_ids):
        assert isinstance(cluster_node, ClusterNode)
        self.analysis_name = analysis_name  # self.analysis = AnalysisType(analysis)
        self.df_full = df_full
        self.cluster_node = cluster_node
        self.id = self.cluster_node.get_id()
        self.dist = self.cluster_node.dist
        self.ypos = self.dist  # alias
        self.is_leaf = self.cluster_node.is_leaf()
        self.num_leaves = self.cluster_node.get_count()
        self.leaf_ids = self.cluster_node.pre_order(lambda x: x.id)
        self.avg_distribution = self.df_full.iloc[self.leaf_ids].mean()  #  average distribution of all leaf nodes
        # if self.analysis_name == "pc_freqs":
        #     self.avg_pc_freq_distribution = PCFreqDistribution(self.avg_distribution)
        # elif self.analysis_name == "pc_tendencies":
        #     self.avg_pc_tendency_distribution = PCTendencyDistribution(self.avg_distribution)
        # else:
        #     raise NotImplementedError()

        if self.is_leaf:
            self.descr = self.df_full.index[self.id]
        else:
            self.descr = f"Cluster #{self.id}\n({self.num_leaves} leaves)"

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
