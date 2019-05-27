from enum import Enum

__all__ = ["IntervalType"]


class IntervalType(str, Enum):
    COMMON_TONE = "common_tone"
    STEP = "step"
    LEAP = "leap"

    @property
    def str_value(self):
        return self.value

    @property
    def label_for_plots(self):
        return self.value


IntervalType.allowed_values = list(IntervalType)
