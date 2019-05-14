from .analysis_spec import FullAnalysisSpec
from .config import ChantStatsConfig
from .dendrogram import plot_dendrogram
from .logging import logger
from .modal_category import GroupingByModalCategory
from .plainchant_sequence_piece import load_plainchant_sequence_pieces, load_pieces
from .plainchant_sequence_monomodal_sections import MonomodalSection, extract_monomodal_sections
from .phrase_collection import PhraseCollection
from .results_export_OLD import export_dendrogram_and_stacked_bar_chart

__all__ = [
    "FullAnalysisSpec",
    "PhraseCollection",
    "GroupingByModalCategory",
    "ChantStatsConfig",
    "load_pieces",
    "load_plainchant_sequence_pieces",
    "logger",
    "chantstats_logger",
    "plot_dendrogram",
    "export_dendrogram_and_stacked_bar_chart",
]

chantstats_logger = logger  # alias for convenience

# Set __version__ attribute (via versioneer)
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
