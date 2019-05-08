from functools import lru_cache

from .analysis_spec import RepertoireAndGenreType
from .plainchant_sequence_piece import load_plainchant_sequence_pieces


class ChantStatsConfig:
    def __init__(self, musicxml_paths):
        self.musicxml_paths = {RepertoireAndGenreType(key): path for (key, path) in musicxml_paths.items()}

    def get_musicxml_path(self, repertoire_and_genre):
        rep_and_genre = RepertoireAndGenreType(repertoire_and_genre)
        musicxml_path = self.musicxml_paths[rep_and_genre]
        return musicxml_path

    @lru_cache(maxsize=10)
    def load_pieces(self, repertoire_and_genre, *, pattern=None):
        musicxml_path = self.get_musicxml_path(repertoire_and_genre)

        if repertoire_and_genre == "plainchant_sequences":
            pieces = load_plainchant_sequence_pieces(musicxml_path, pattern=pattern)
        else:
            raise NotImplementedError()
        return pieces
