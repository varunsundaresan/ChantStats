import os
import pandas as pd
import shutil
from collections import defaultdict
from enum import Enum

from .ambitus import AmbitusType
from .dendrogram import make_dendrogram_tree
from .logging import logger

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

    def get_output_path_stub(self, key):
        if self == "final":
            return os.path.join("by_final", f"{key}_final")
        elif self == "final_and_ambitus":
            final = key[0]
            ambitus = AmbitusType(key[1])
            return os.path.join(f"{ambitus}_modes", f"{final}_{ambitus}")
        else:
            raise NotImplementedError(f"Unexpected grouping type: {self}")

    def get_descr(self, key):
        if self == "final":
            return os.path.join(f"{key}_final")
        elif self == "final_and_ambitus":
            final = key[0]
            ambitus = AmbitusType(key[1])
            return os.path.join(f"{final}_{ambitus}")
        else:
            raise NotImplementedError(f"Unexpected grouping type: {self}")


class ModalCategory:
    def __init__(self, items, modal_category_type, key):
        self.items = items
        self.modal_category_type = ModalCategoryType(modal_category_type)
        self.key = key
        self.output_path_stub = self.modal_category_type.get_output_path_stub(self.key)
        self.descr = self.modal_category_type.get_descr(self.key)

    def __repr__(self):
        return f"<ModalCategory with {self.modal_category_type.value}={self.key}, {len(self.items)} items>"

    def make_results_dataframe(self, *, analysis_func):
        return pd.DataFrame({x.descr: analysis_func(x) for x in self.items}).T

    def export_results(self, *, analysis_func, output_dir, fmt="png", p_cutoff=0.15):
        cur_output_dir = os.path.join(output_dir, self.output_path_stub)
        # logger.debug(f"Exporting results for key={grp.key!r} to directory: '{cur_output_dir}'")
        logger.debug(f"Current output dir (for key={self.key!r}): '{cur_output_dir}'")
        df = self.make_results_dataframe(analysis_func=analysis_func)
        tree = make_dendrogram_tree(df)
        tree.export_dendrogram(cur_output_dir, fmt=fmt)
        for node in tree.get_max_nodes_below_cutoff(p_cutoff=p_cutoff):
            node.export_barplot(cur_output_dir, fmt=fmt)


class GroupingByModalCategory:
    """
    Represents
    """

    def __init__(self, items, *, group_by):
        self.items = items
        self.grouped_by = ModalCategoryType(group_by)
        self.grouping_func = self.grouped_by.grouping_func

        grps = defaultdict(list)
        for item in self.items:
            grps[self.grouping_func(item)].append(item)
        self.groups = {key: ModalCategory(items, self.grouped_by, key) for key, items in grps.items()}
        self.keys = list(sorted(self.groups.keys()))

    def __repr__(self):
        return f"<Grouping by '{self.grouped_by}': {len(self.groups)} groups ({len(self.items)} items)>"

    def export_results(self, *, analysis_func, output_dir, fmt="png", p_cutoff=0.15, overwrite=False):
        if os.path.exists(output_dir):
            logger.info(f"Output directory exists: '{output_dir}'")
            if overwrite:
                logger.debug("Deleting its contents and re-exporting results because overwrite=True.")
                shutil.rmtree(output_dir)
            else:
                logger.info(
                    f"Not exporting results (use `overwrite=True` to delete its contents and re-export the results)."
                )
                return

        for grp in self.groups.values():
            grp.export_results(analysis_func=analysis_func, output_dir=output_dir, fmt=fmt, p_cutoff=p_cutoff)
