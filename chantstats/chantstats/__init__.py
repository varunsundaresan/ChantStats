from .logging import logger
from .piece import load_plainchant_sequence_pieces

chantstats_logger = logger  # alias for convenience

# Set __version__ attribute (via versioneer)
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
