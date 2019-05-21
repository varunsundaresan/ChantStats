from enum import Enum
from .ambitus import AmbitusType

__all__ = ["ModalCategoryType"]


class ModalCategoryType(str, Enum):
    FINAL = "final"
    FINAL_AND_AMBITUS = "final_and_ambitus"

    @property
    def grouping_func(self):
        if self == "final":
            return lambda x: x.final
        elif self == "final_and_ambitus":
            return lambda x: (x.final, x.ambitus)
        else:  # pragma: no cover
            raise NotImplementedError(f"Unexpected grouping type: {self}")

    @property
    def enforce_same_ambitus(self):
        if self == "final":
            return False
        elif self == "final_and_ambitus":
            return True
        else:  # pragma: no cover
            raise NotImplementedError(f"Unexpected grouping type: {self}")

    def get_output_path_stub_1(self, key):
        if self == "final":
            return "by_final"
        elif self == "final_and_ambitus":
            ambitus = AmbitusType(key[1])
            return f"{ambitus}_modes"
        else:  # pragma: no cover
            raise NotImplementedError(f"Unexpected grouping type: {self}")

    def get_output_path_stub_2(self, key):
        if self == "final":
            return f"{key}_final"
        elif self == "final_and_ambitus":
            final = key[0]
            ambitus = AmbitusType(key[1])
            return f"{final}_{ambitus}"
        else:  # pragma: no cover
            raise NotImplementedError(f"Unexpected grouping type: {self}")

    def get_descr(self, key):
        if self == "final":
            return f"{key}-final"
        elif self == "final_and_ambitus":
            final = key[0]
            ambitus = AmbitusType(key[1])
            return f"{final}-{ambitus}"
        else:  # pragma: no cover
            raise NotImplementedError(f"Unexpected grouping type: {self}")
