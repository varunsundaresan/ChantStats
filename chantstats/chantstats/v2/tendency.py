import pandas as pd
from .note_pair import NotePair

__all__ = ["BaseTendencies", "PCTendencies", "PCApproaches"]


class BaseTendencies:
    def __init__(self, pairs, *, label_first, label_second):
        first_items, second_items = zip(*pairs)
        df = pd.DataFrame({label_first: first_items, label_second: second_items, "count": 1}).dropna()
        cls_first = first_items[0].__class__
        cls_second = second_items[0].__class__
        df_pivot_table = df.pivot_table(
            index=label_second, columns=label_first, values="count", aggfunc=sum, fill_value=0
        )
        self.df_pair_counts = (
            df_pivot_table.reindex(cls_second.allowed_values)
            .fillna(0, downcast="infer")
            .reindex(cls_first.allowed_values, axis=1)
            .fillna(0, downcast="infer")
        )
        # TODO: verify that we are not accidentally dropping values by reindexing (and add some safety measure for this if needed)

        sums_per_col = self.df_pair_counts.sum(axis="index", skipna=False)
        self.df_condprobs_v1 = 100 * self.df_pair_counts.div(sums_per_col, axis="columns")  # each column sums up to 100

        # sums_per_row = self.df_pair_counts.sum(axis="columns", skipna=False)
        # self.df_condprobs_v2 = 100 * self.df_pair_counts.div(sums_per_col, axis="columns")  # each column sums up to 100

    def as_series(self, using):
        if using == "counts":
            res = self.df_pair_counts
        elif using == "condprobs_v1":
            res = self.df_condprobs_v1
        else:
            raise ValueError(f"Invalid value: '{using}'. Must be one of ['counts', 'condprobs_v1'].")

        return res.unstack()  # same as the dataframe, but as a series with a hierarchical index


class PCTendencies(BaseTendencies):
    def __init__(cls, item):
        super().__init__(item.pc_pairs, label_first="pc1", label_second="pc2")


class ModeDegreeTendencies(BaseTendencies):
    def __init__(cls, item):
        super().__init__(item.mode_degree_pairs, label_first="pc1", label_second="pc2")


class PCApproaches(BaseTendencies):
    def __init__(cls, item):
        second_pcs = [pc2 for (_, pc2) in item.pc_pairs]
        approach_interval_types = [NotePair(n1, n2).interval_type_v1 for (n1, n2) in item.note_pairs]
        pairs = zip(second_pcs, approach_interval_types)
        super().__init__(pairs, label_first="pc2", label_second="approach")
