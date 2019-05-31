import pandas as pd
from itertools import tee


def group_by_contiguous_values(df, col):
    """
    Group pandas dataframe `df` by contiguous values in column `col`.
    Alternatively, `col` can also be a pandas Series.

    Example:

        >>> df = pd.DataFrame({
        ...     'col1': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        ...     'col2': ['a', 'a', 'a', 'b', 'c', 'c', 'c', 'c', 'd', 'd']
        ...     })
        >>> for i, grp in group_by_contiguous_values(df, 'col2'):
        ...     print('Group {}: {}'.format(i, list(grp.col1)))
        ...
        Group 0: [10, 20, 30]
        Group 1: [40]
        Group 2: [50, 60, 70, 80]
        Group 3: [90, 100]
    """
    s = col if isinstance(col, pd.Series) else df[col]
    value_groups = (s != s.shift(1).bfill()).astype(int).cumsum()
    return df.groupby(value_groups)


def pairwise(it):
    it1, it2 = tee(it)
    next(it2)
    return list(zip(it1, it2))
