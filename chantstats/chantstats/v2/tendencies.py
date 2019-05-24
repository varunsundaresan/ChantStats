import pandas as pd

__all__ = ["BaseTendencies"]


class BaseTendencies:
    def __init__(self, df_pair_counts, cls_first, cls_second):
        self.cls_first = cls_first
        self.cls_second = cls_second
        assert isinstance(df_pair_counts, pd.DataFrame)
        assert set(df_pair_counts.columns) == set(self.cls_first.allowed_values)
        assert set(df_pair_counts.index) == set(self.cls_second.allowed_values)
        self.df_pair_counts = df_pair_counts

        sums_per_col = self.df_pair_counts.sum(axis="index", skipna=False)
        self.df_condprobs_v1 = 100 * self.df_pair_counts.div(sums_per_col, axis="columns")  # each column sums up to 100

        # sums_per_row = self.df_pair_counts.sum(axis="columns", skipna=False)
        # self.df_condprobs_v2 = 100 * self.df_pair_counts.div(sums_per_col, axis="columns")  # each column sums up to 100

    @classmethod
    def from_pairs(cls, pairs, *, label_first, label_second):
        first_items, second_items = zip(*pairs)
        df = pd.DataFrame({label_first: first_items, label_second: second_items, "count": 1}).dropna()
        cls_first = first_items[0].__class__
        cls_second = second_items[0].__class__
        df_pivot_table = df.pivot_table(
            index=label_second, columns=label_first, values="count", aggfunc=sum, fill_value=0
        )
        df_pair_counts = (
            df_pivot_table.reindex(cls_second.allowed_values)
            .fillna(0, downcast="infer")
            .reindex(cls_first.allowed_values, axis=1)
            .fillna(0, downcast="infer")
        )
        # TODO: verify that we are not accidentally dropping values by reindexing (and add some safety measure for this if needed)

        return cls(df_pair_counts, cls_first, cls_second)
