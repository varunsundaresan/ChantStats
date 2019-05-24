from enum import Enum

__all__ = ["IntervalType"]


class IntervalType(str, Enum):
    COMMON_TONE = "common_tone"
    STEP = "step"
    LEAP = "leap"


IntervalType.allowed_values = list(IntervalType)
