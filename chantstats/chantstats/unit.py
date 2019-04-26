from enum import Enum


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


class UnitType(EnumWithDescription):
    PCS = ("pcs", "pitch classes")
    MODE_DEGREES = ("mode_degrees", "mode degrees")
