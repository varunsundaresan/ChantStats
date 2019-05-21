import pandas as pd
from collections import defaultdict
from enum import Enum
from .ambitus import AmbitusType
from .logging import logger

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


class ModalCategory:
    """
    Represents a "modal category".
    """

    def __init__(self, items, modal_category_type, key):
        self.items = items
        self.modal_category_type = ModalCategoryType(modal_category_type)
        self.key = key
        self.output_path_stub_1 = self.modal_category_type.get_output_path_stub_1(self.key)
        self.output_path_stub_2 = self.modal_category_type.get_output_path_stub_2(self.key)
        self.descr = self.modal_category_type.get_descr(self.key)

    def __repr__(self):
        return f"<ModalCategory with {self.modal_category_type.value}={self.key}, {len(self.items)} items>"

    def make_results_dataframe(self, *, analysis_func, unit):
        df = pd.DataFrame({x.descr: analysis_func(x, unit=unit) for x in self.items}).T
        if unit == "pcs":
            # column labels are already strings; nothing to do
            pass
        elif unit == "mode_degrees":
            logger.debug("Converting column labels from mode degrees to strings.")
            df.columns = [x.descr for x in df.columns]
        else:
            raise NotImplementedError()
        return df


class GroupingByModalCategory:
    """
    Represents
    """

    def __init__(self, items, *, group_by):
        self._items = items
        self.grouped_by = ModalCategoryType(group_by)
        self.grouping_func = self.grouped_by.grouping_func

        grps = defaultdict(list)
        for item in self._items:
            grps[self.grouping_func(item)].append(item)
        self.groups = {key: ModalCategory(items, self.grouped_by, key) for key, items in grps.items()}
        self.keys = list(sorted(self.groups.keys()))

    def __repr__(self):
        s = f"<Grouping by '{self.grouped_by}' with {len(self.groups)} groups ({len(self._items)} items):\n"
        for key, grp in self.groups.items():
            s += f"   {key!r}: {grp}\n"
        s += f">"
        return s

    def __getitem__(self, key):
        return self.groups[key]
