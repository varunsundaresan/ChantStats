from .dendrogram import plot_dendrogram
from .logging import logger
from .plainchant_sequence_piece import load_plainchant_sequence_pieces
from .phrase_collection import PhraseCollection

__all__ = ["PhraseCollection", "load_plainchant_sequence_pieces", "logger", "chantstats_logger", "plot_dendrogram"]

chantstats_logger = logger  # alias for convenience

# Set __version__ attribute (via versioneer)
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
