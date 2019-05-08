import os
import pandas as pd
from collections import defaultdict
from enum import Enum

from .ambitus import AmbitusType
from .logging import logger
from .results_export import export_dendrogram_and_stacked_bar_chart

__all__ = ["GroupingByModalCategory"]


class ModalCategoryType(str, Enum):
    FINAL = "final"
    FINAL_AND_AMBITUS = "final_and_ambitus"

    @property
    def grouping_func(self):
        if self == "final":
            return lambda x: x.final
        elif self == "final_and_ambitus":
            return lambda x: (x.final, x.ambitus)
        else:
            raise NotImplementedError(f"Unexpected grouping type: {self}")

    def get_output_path_stub_1(self, key):
        if self == "final":
            return "by_final"
        elif self == "final_and_ambitus":
            final = key[0]
            ambitus = AmbitusType(key[1])
            return f"{ambitus}_modes"
        else:
            raise NotImplementedError(f"Unexpected grouping type: {self}")

    def get_output_path_stub_2(self, key):
        if self == "final":
            return f"{key}_final"
        elif self == "final_and_ambitus":
            final = key[0]
            ambitus = AmbitusType(key[1])
            return f"{final}_{ambitus}"
        else:
            raise NotImplementedError(f"Unexpected grouping type: {self}")

    def get_descr(self, key):
        if self == "final":
            return os.path.join(f"{key}-final")
        elif self == "final_and_ambitus":
            final = key[0]
            ambitus = AmbitusType(key[1])
            return os.path.join(f"{final}-{ambitus}")
        else:
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
        return pd.DataFrame({x.descr: analysis_func(x, unit=unit) for x in self.items}).T


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

    def export_results(
        self, *, analysis_spec, output_root_dir, p_cutoff, unit, overwrite=False, sort_freqs_ascending=False
    ):
        logger.info(f"Exporting results for {self}")
        for modal_category in self.groups.values():
            export_dendrogram_and_stacked_bar_chart(
                output_root_dir=output_root_dir,
                analysis_spec=analysis_spec,
                modal_category=modal_category,
                p_cutoff=p_cutoff,
                unit=unit,
                sort_freqs_ascending=sort_freqs_ascending,
                overwrite=overwrite,
            )
