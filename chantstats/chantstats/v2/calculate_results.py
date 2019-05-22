from .analysis_functions import AnalysisType
from .dendrogram import calculate_dendrogram
from .logging import logger
from .modal_category import ModalCategoryType, GroupingByModalCategory
from .plainchant_sequence_piece import load_pieces
from .repertoire_and_genre import RepertoireAndGenreType
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


def calculate_results(
    repertoire_and_genre, analysis, cfg, pieces=None, min_length_monomodal_sections=3, modes=None, units=None
):
    results = {}

    pieces = pieces or load_pieces(repertoire_and_genre, cfg)
    modes = modes or list(ModalCategoryType)
    units = units or list(UnitType)

    for mode in modes:
        analysis_inputs = pieces.get_analysis_inputs(mode, min_length_monomodal_sections=min_length_monomodal_sections)
        grouping = GroupingByModalCategory(analysis_inputs, group_by=mode)
        for modal_category in grouping.groups.values():
            logger.info(f"Calculating {analysis} results for {modal_category}")
            for unit in units:
                dendrogram = calculate_dendrogram(modal_category, analysis=analysis, unit=unit)
                path_stubs = PathStubs(repertoire_and_genre, analysis, unit, modal_category)
                results[path_stubs] = {"dendrogram": dendrogram}

    return results
