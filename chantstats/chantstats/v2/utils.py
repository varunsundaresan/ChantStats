import numpy as np
from enum import Enum

__all__ = ["EnumWithDescription"]


class EnumWithDescription(str, Enum):
    def __new__(cls, name, desc, **kwargs):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj._description = desc
        return obj

    @property
    def description(self) -> str:
        """
        Returns
        -------
        str
            Long form description of this enum suitable for use in plot titles etc.
        """
        return self._description


def is_close_to_zero_or_100(x):
    return np.isclose(x, 0.0) or np.isclose(x, 100.0)
