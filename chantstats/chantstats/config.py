from .analysis_spec import RepertoireAndGenreType


class ChantStatsConfig:
    def __init__(self, musicxml_paths):
        self.musicxml_paths = {RepertoireAndGenreType(key): path for (key, path) in musicxml_paths.items()}

    def get_musicxml_path(self, repertoire_and_genre):
        rep_and_genre = RepertoireAndGenreType(repertoire_and_genre)
        musicxml_path = self.musicxml_paths[rep_and_genre]
        return musicxml_path

    def load_pieces(self, repertoire_and_genre, *, pattern=None):
        raise DeprecationWarning("This method is deprecated. Use the function 'load_pieces()' instead.")
