import pandas as pd

# from .note_pair import NotePair

__all__ = ["BaseTendencies"]


class BaseTendencies:
    def __init__(self, first_items, second_items, *, label_first, label_second):
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
        first_pcs = item.pitch_classes[:-1]
        second_pcs = item.pitch_classes[1:]
        super().__init__(first_pcs, second_pcs, label_first="pc1", label_second="pc2")
