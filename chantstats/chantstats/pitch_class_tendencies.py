import pandas as pd
from .pitch_class_freqs import OCCURRING_PCS

__all__ = ["PCTendencies"]


class classproperty(object):
    # See https://stackoverflow.com/questions/5189699/how-to-make-a-class-property
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class PCTendencies:
    ALLOWED_VALUES = OCCURRING_PCS

    def __init__(self, df_pair_counts):
        assert isinstance(df_pair_counts, pd.DataFrame)
        assert set(df_pair_counts.index) == set(self.ALLOWED_VALUES)
        assert set(df_pair_counts.columns) == set(self.ALLOWED_VALUES)
        self.df_pair_counts = df_pair_counts

        sums_per_col = self.df_pair_counts.sum(axis="index", skipna=False)
        self.df_condprobs_v1 = 100 * self.df_pair_counts.div(sums_per_col, axis="columns")  # each column sums up to 100

        # sums_per_row = self.df_pair_counts.sum(axis="columns", skipna=False)
        # self.df_condprobs_v2 = 100 * self.df_pair_counts.div(sums_per_col, axis="columns")  # each column sums up to 100

    @classmethod
    def from_pitch_classes(cls, pcs):
        assert set(pcs).issubset(cls.ALLOWED_VALUES)
        s = pd.Series(pcs)
        df = pd.DataFrame({"pc_A": s, "pc_B": s.shift(-1), "count": 1}).dropna()
        df_pair_counts = (
            df.pivot_table(index="pc_B", columns="pc_A", values="count", aggfunc=sum, fill_value=0)
            .reindex(cls.ALLOWED_VALUES)
            .fillna(0, downcast="infer")
            .reindex(cls.ALLOWED_VALUES, axis=1)
            .fillna(0, downcast="infer")
        )
        return cls(df_pair_counts)

    @classproperty
    def zeros(cls):
        # initialise the class with an empty list to obtain a "zero values" object
        df_pair_counts = pd.DataFrame(0, index=OCCURRING_PCS, columns=OCCURRING_PCS)
        return PCTendencies(df_pair_counts)

    def __add__(self, other):
        cls = self.__class__
        assert isinstance(other, cls)
        return cls(self.df_pair_counts + other.df_pair_counts)

    def get_condprobs_v1(self, given_pc):
        return self.df_condprobs_v1[given_pc]

    # @property
    # def condprobs_v1(self):
    #     df = self.df_pair_counts
    #     sums_per_col = df.sum(axis="index", skipna=False)
    #     condprobs_v1 = df.div(sums_per_col, axis="columns")  # each column sums up to 1.0
    #     return condprobs_v1
    #
    # @property
    # def condprobs_v2(self):
    #     df = self.df_pair_counts
    #     sums_per_row = df.sum(axis="columns", skipna=False)
    #     condprobs_v2 = df.div(sums_per_row, axis="index")  # each row sums up to 1.0
    #     return condprobs_v2
