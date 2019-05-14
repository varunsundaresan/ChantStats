from .analysis_spec import RepertoireAndGenreType, AnalysisType
from .dendrogram2 import Dendrogram
from .logging import logger
from .modal_category import ModalCategoryType, GroupingByModalCategory
from .plainchant_sequence_piece import load_pieces
from .unit import UnitType

__all__ = ["calculate_results"]


class PathStubs(tuple):
    def __new__(cls, repertoire_and_genre, analysis, unit, modal_category):
        rep_and_genre = RepertoireAndGenreType(repertoire_and_genre)
        analysis = AnalysisType(analysis)
        unit = UnitType(unit)
        modal_category = modal_category

        path_stubs = (
            rep_and_genre.output_path_stub_1,
            analysis.output_path_stub,
            rep_and_genre.output_path_stub_2,
            unit.output_path_stub,
            modal_category.output_path_stub_1,
            modal_category.output_path_stub_2,
        )

        obj = tuple.__new__(cls, path_stubs)
        obj.rep_and_genre = rep_and_genre
        obj.analysis = analysis
        obj.unit = unit
        obj.modal_category = modal_category
        obj.path_stubs = path_stubs
        obj.path_stubs_without_unit_and_mode = path_stubs[:3]

        return obj


def calculate_pc_freqs(analysis_input, unit):
    if unit == "pcs":
        # freqs = PCFreqs(analysis_input.pc)
        freqs = analysis_input.pc_freqs.rel_freqs
    elif unit == "mode_degrees":
        # freqs = ModeDegreeFreqs(analysis_input.mode_degrees)
        freqs = analysis_input.mode_degree_freqs.rel_freqs
    else:
        raise NotImplementedError()

    return freqs


def calculate_pc_tendencies(analysis_input, unit):
    if unit == "pcs":
        freqs = analysis_input.pc_tendencies.condprobs_v1
    elif unit == "mode_degrees":
        raise NotImplementedError("TODO")
    else:
        raise NotImplementedError()

    return freqs.fillna(0).unstack()


def get_analysis_function(analysis):
    if analysis == "pc_freqs":
        return calculate_pc_freqs
    elif analysis == "pc_tendencies":
        return calculate_pc_tendencies
    else:
        raise NotImplementedError()


def calculate_dendrogram(modal_category, *, analysis_name, unit):
    unit = UnitType(unit)
    analysis_func = get_analysis_function(analysis_name)
    df = modal_category.make_results_dataframe(analysis_func=analysis_func, unit=unit)
    # df = df[[col for col in df.columns[(df != 0).any()]]]  # remove columns where all values are zero
    dendrogram = Dendrogram(df, analysis_name=analysis_name)
    return dendrogram


def calculate_results(
    repertoire_and_genre, analysis_name, cfg, min_length_monomodal_sections=3, modes=None, units=None
):
    results = {}

    pieces = load_pieces(repertoire_and_genre, cfg)
    modes = modes or list(ModalCategoryType)
    units = units or list(UnitType)

    for mode in modes:
        analysis_inputs = pieces.get_analysis_inputs(mode, min_length_monomodal_sections=min_length_monomodal_sections)
        grouping = GroupingByModalCategory(analysis_inputs, group_by=mode)
        for modal_category in grouping.groups.values():
            logger.info(f"Calculating {analysis_name} results for {modal_category}")
            for unit in units:
                dendrogram = calculate_dendrogram(modal_category, analysis_name=analysis_name, unit=unit)
                path_stubs = PathStubs(repertoire_and_genre, analysis_name, unit, modal_category)
                results[path_stubs] = {"dendrogram": dendrogram}

    return results
