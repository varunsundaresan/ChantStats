import os
import pandas as pd
import shutil
from collections import defaultdict
from enum import Enum

from .ambitus import AmbitusType
from .dendrogram2 import Dendrogram
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
            return os.path.join(f"{key}-final")
        elif self == "final_and_ambitus":
            final = key[0]
            ambitus = AmbitusType(key[1])
            return os.path.join(f"{final}-{ambitus}")
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

    def export_dendrogram_and_stacked_bar_chart(
        self, *, output_root_dir, analysis_spec, p_cutoff, sort_freqs_ascending=False, overwrite=False
    ):
        """
        Export dendrogram and stacked bar chart for this modal category.

        Parameters
        ----------
        output_root_dir : str
            The path under which to export results. Note that the actual directory
            where the plots are saved will be a sub-directory of this root directory,
            for example: `<output_root_dir>/authentic_modes/G_authentic`.
        analysis_spec : FullAnalysisSpec
        p_cutoff : float
        sort_freqs_ascending : bool, optional
        overwrite: book, optional
        """
        logger.info(f"Exporting results for {self}")

        output_dir = analysis_spec.output_path(root_dir=output_root_dir, modal_category=self)
        if os.path.exists(output_dir):
            if not overwrite:
                logger.warning(
                    f"Output directory exists. Use `overwrite=True` to delete its contents before exporting results: '{output_dir}'"
                )
                return
            else:
                logger.warning(
                    f"Deleting contents of existing output directory (because overwrite=True): '{output_dir}'"
                )
                shutil.rmtree(output_dir)
        if not os.path.exists(output_dir):
            logger.debug(f"Creating output dir: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)

        df = self.make_results_dataframe(analysis_func=analysis_spec.analysis_func)
        dendrogram = Dendrogram(df, p_threshold=p_cutoff)

        output_filename = os.path.join(output_dir, "dendrogram.png")
        title = f"Dendrogram: {analysis_spec.get_description(modal_category=self)} (p_cutoff={p_cutoff})"
        fig = dendrogram.plot_dendrogram(title=title)
        fig.savefig(output_filename)
        logger.debug(f"Saved dendrogram plot: '{output_filename}'")

        output_filename = os.path.join(output_dir, "stacked_bar_chart.png")
        title = f"{analysis_spec.get_description(modal_category=self)} (p_cutoff={p_cutoff})"
        fig = dendrogram.plot_stacked_bar_charts(title=title, sort_freqs_ascending=sort_freqs_ascending)
        fig.savefig(output_filename)
        logger.debug(f"Saved stacked bar chart: '{output_filename}'")


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

    def export_results(self, *, analysis_spec, output_root_dir, p_cutoff, overwrite=False, sort_freqs_ascending=False):
        if os.path.exists(output_root_dir):
            if not overwrite:
                logger.warning(
                    f"Output directory exists. Use `overwrite=True` to delete its contents before exporting results: '{output_root_dir}'"
                )
                return
            else:
                logger.warning(
                    f"Deleting contents of existing output directory (because overwrite=True): '{output_root_dir}'"
                )
                shutil.rmtree(output_root_dir)

        logger.info(f"Exporting results for {self}")
        for group in self.groups.values():
            group.export_dendrogram_and_stacked_bar_chart(
                analysis_spec=analysis_spec,
                output_root_dir=output_root_dir,
                p_cutoff=p_cutoff,
                sort_freqs_ascending=sort_freqs_ascending,
            )
