import os
import pickle
import shutil
from collections import defaultdict
from tqdm import tqdm

from .analysis_spec import RepertoireAndGenreType, AnalysisType, AnalysisFuncPCFreqs
from .config import ChantStatsConfig
from .dendrogram2 import Dendrogram
from .logging import logger
from .modal_category import ModalCategoryType, GroupingByModalCategory
from .unit import UnitType
from .plainchant_sequence_monomodal_sections import extract_monomodal_sections
from .results_export import get_color_palette_for_unit

__all__ = []


def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)


def get_recursive_subdict(the_dict, keys):
    first_key = keys[0]
    if len(keys) == 1:
        return the_dict[first_key]
    elif len(keys) > 1:
        return get_recursive_subdict(the_dict[first_key], keys[1:])
    else:
        raise RuntimeError()


def convert_to_nested_dict(d):
    if not isinstance(d, dict):
        return d
    else:
        return {key: convert_to_nested_dict(val) for key, val in d.items()}


class AnalysisResultCollection:
    def __init__(self, cfg):
        assert isinstance(cfg, ChantStatsConfig)
        self.cfg = cfg
        self._results = defaultdict(dict)
        self._results_json = defaultdict(dict)

        # The following two are redundant (could compute from the above two on the fly), but nice to have
        self._results_nested = recursive_defaultdict()
        self._results_nested_json = recursive_defaultdict()

        self.all_pieces = {}
        self._load_pieces_if_needed("plainchant_sequences")

    def __getitem__(self, path_stubs):
        return self._results[path_stubs]

    def _get_path_stubs(self, repertoire_and_genre, analysis, unit, modal_category):
        rep_and_genre = RepertoireAndGenreType(repertoire_and_genre)
        analysis = AnalysisType(analysis)
        unit = UnitType(unit)
        return (
            rep_and_genre.output_path_stub_1,
            analysis.output_path_stub,
            rep_and_genre.output_path_stub_2,
            unit.output_path_stub,
            modal_category.output_path_stub_1,
            modal_category.output_path_stub_2,
        )

    def _load_pieces_if_needed(self, repertoire_and_genre):
        if repertoire_and_genre == "plainchant_sequences":
            if "plainchant_sequences" not in self.all_pieces.keys():
                self.all_pieces["plainchant_sequences"] = PlainchantSequencePieces.from_musicxml_files(self.cfg)
        else:
            raise NotImplementedError(
                "TODO: when initialising AnalysisResultCollection, load pieces for all rep/genre types, not just plainchant sequences!"
            )

    def accumulate_results(
        self, repertoire_and_genre, analysis, unit, mode, min_length_monomodal_sections=3, p_cutoff=0.7
    ):
        self._load_pieces_if_needed(repertoire_and_genre)

        pieces = self.all_pieces[repertoire_and_genre]
        analysis_inputs = pieces.get_analysis_inputs(mode, min_length_monomodal_sections=min_length_monomodal_sections)

        grouping = GroupingByModalCategory(analysis_inputs, group_by=mode)
        logger.debug(f"Calculating results for {grouping}")
        for key in tqdm(grouping.keys):
            modal_category = grouping[key]
            df = modal_category.make_results_dataframe(analysis_func=AnalysisFuncPCFreqs("rel_freqs"), unit=unit)
            dendrogram = Dendrogram(df, p_threshold=p_cutoff)

            self.insert_results(repertoire_and_genre, analysis, unit, modal_category, "dendrogram", dendrogram)
            self.insert_results(
                repertoire_and_genre,
                analysis,
                unit,
                modal_category,
                "clusters",
                [c for c in dendrogram.nodes_below_cutoff],
            )

    def insert_results(self, repertoire_and_genre, analysis, unit, modal_category, results_key, value):
        if isinstance(value, list):
            value_json = [x.to_json() for x in value]
        else:
            value_json = value.to_json()

        path_stubs = self._get_path_stubs(repertoire_and_genre, analysis, unit, modal_category)

        get_recursive_subdict(self._results_nested, path_stubs)[results_key] = value
        get_recursive_subdict(self._results_nested_json, path_stubs)[results_key] = value_json
        self._results[path_stubs][results_key] = value
        self._results_json[path_stubs][results_key] = value_json

    def to_dict(self):
        return dict(self._results_json)  # convert from defaultdict to dict

    def to_nested_dict(self):
        return convert_to_nested_dict(self._results_nested_json)

    def dump(self, filename, overwrite=False):
        if os.path.exists(filename):
            if not overwrite:
                logger.warn(f"Not overwriting existing file: '{filename}' (use 'overwrite=True' to overwrite)")
                return
            else:
                logger.warn(f"Overwriting existing file: '{filename}'")

        data = {
            "cfg": self.cfg,
            "_results": self._results,
            "_results_json": self._results_json,
            "_results_nested": self._results_nested,
            "_results_nested_json": self._results_nested_json,
        }

        with open(filename, "wb") as f:
            pickle.dump(data, f)

    @classmethod
    def load(cls, filename):
        with open(filename, "rb") as f:
            data = pickle.load(f)

        cfg = data.pop("cfg")
        results = cls(cfg)
        results.__dict__.update(data)
        return results

    def export_plots(self, output_root_dir, overwrite=False):
        if os.path.exists(output_root_dir):
            if not overwrite:
                logger.warn(f"Aborting because output root dir already exists: '{output_root_dir}'")
                logger.warn(f"Use 'overwrite=True' to overwrite existing results.")
                return
            else:
                logger.warn(f"Removing existing output root dir: {output_root_dir}")
                shutil.rmtree(output_root_dir)

        for path_stubs in self.to_dict().keys():
            output_dir = os.path.join(output_root_dir, *path_stubs)
            logger.info(f"Exporting results to folder: {output_dir}")

            dendrogram = self._results[path_stubs]["dendrogram"]

            # Export dendrogram
            os.makedirs(output_dir, exist_ok=True)
            fig = dendrogram.plot_dendrogram()
            fig.savefig(os.path.join(output_dir, "dendrogram.png"))

            # Export stacked bar chart
            unit = path_stubs[3]
            color_palette = get_color_palette_for_unit(unit)
            fig = dendrogram.plot_stacked_bar_charts(color_palette=color_palette)
            fig.savefig(os.path.join(output_dir, "stacked_bar_chart.png"))


from .plainchant_sequence_piece import PlainchantSequencePiece


class PlainchantSequencePieces:
    def __init__(self, pieces):
        assert all([isinstance(p, PlainchantSequencePiece) for p in pieces])
        self.pieces = pieces
        self.repertoire_and_genre = RepertoireAndGenreType("plainchant_sequences")

    def __repr__(self):
        return f"<Collection of {len(self.pieces)} plainchant sequence pieces>"

    @classmethod
    def from_musicxml_files(cls, cfg, filename_pattern=None):
        pieces = cfg.load_pieces("plainchant_sequences", pattern=filename_pattern)
        return cls(pieces)

    def get_analysis_inputs(self, mode, min_length_monomodal_sections=3):
        mode = ModalCategoryType(mode)
        return extract_monomodal_sections(
            self.pieces, enforce_same_ambitus=mode.enforce_same_ambitus, min_length=min_length_monomodal_sections
        )


#
# def prepare_analysis_inputs(repertoire_and_genre, mode, *, cfg, min_length_monomodal_sections=3, filename_pattern=None):
#     pieces = cfg.load_pieces(repertoire_and_genre, pattern=filename_pattern)
#     mode = ModalCategoryType(mode)
#
#     enforce_same_ambitus = {"final": False, "final_and_ambitus": True}[mode]
#
#     if repertoire_and_genre == "plainchant_sequences":
#         return extract_monomodal_sections(
#             pieces, enforce_same_ambitus=enforce_same_ambitus, min_length=min_length_monomodal_sections
#         )
#     else:
#         raise NotImplementedError(f"Unsupported repertoire/genre: {repertoire_and_genre}")
