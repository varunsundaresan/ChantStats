from collections import defaultdict
from tqdm import tqdm

from .analysis_spec import RepertoireAndGenreType, AnalysisType, AnalysisFuncPCFreqs
from .dendrogram2 import Dendrogram
from .logging import logger
from .modal_category import ModalCategoryType, GroupingByModalCategory
from .unit import UnitType
from .plainchant_sequence_monomodal_sections import extract_monomodal_sections

__all__ = ["prepare_analysis_inputs"]


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
    def __init__(self):
        self._results = defaultdict(dict)
        self._results_nested = recursive_defaultdict()  # TODO: we can calculate it on the fly if needed

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

    #     def get_subdict(self, repertoire_and_genre, analysis, unit, modal_category, results_key, value):
    #         return get_recursive_subdict(self._results, path_stubs)[results_key]

    def to_dict(self):
        return self._results

    def to_nested_dict(self):
        return convert_to_nested_dict(self._results_nested)

    def insert_results(self, repertoire_and_genre, analysis, unit, modal_category, results_key, value):
        path_stubs = self._get_path_stubs(repertoire_and_genre, analysis, unit, modal_category)
        get_recursive_subdict(self._results_nested, path_stubs)[results_key] = value
        self._results[path_stubs][results_key] = value


def prepare_analysis_inputs(repertoire_and_genre, mode, *, cfg, min_length_monomodal_sections=3, filename_pattern=None):
    pieces = cfg.load_pieces(repertoire_and_genre, pattern=filename_pattern)
    mode = ModalCategoryType(mode)

    enforce_same_ambitus = {"final": False, "final_and_ambitus": True}[mode]

    if repertoire_and_genre == "plainchant_sequences":
        return extract_monomodal_sections(
            pieces, enforce_same_ambitus=enforce_same_ambitus, min_length=min_length_monomodal_sections
        )
    else:
        raise NotImplementedError(f"Unsupported repertoire/genre: {repertoire_and_genre}")


def accumulate_results(
    existing_results, cfg, repertoire_and_genre, analysis, unit, mode, min_length_monomodal_sections=3, p_cutoff=0.7
):
    results = existing_results or AnalysisResultCollection()
    analysis_inputs = prepare_analysis_inputs(
        repertoire_and_genre, mode, cfg=cfg, min_length_monomodal_sections=3, filename_pattern=None
    )

    grouping = GroupingByModalCategory(analysis_inputs, group_by=mode)
    logger.debug(f"Calculating results for {grouping}")
    for key in tqdm(grouping.keys):
        modal_category = grouping[key]
        df = modal_category.make_results_dataframe(analysis_func=AnalysisFuncPCFreqs("rel_freqs"), unit=unit)
        dendrogram = Dendrogram(df, p_threshold=p_cutoff)

        results.insert_results(repertoire_and_genre, analysis, unit, modal_category, "dendrogram", dendrogram.to_json())
        results.insert_results(
            repertoire_and_genre,
            analysis,
            unit,
            modal_category,
            "clusters",
            [c.to_json() for c in dendrogram.nodes_below_cutoff],
        )

    return results
