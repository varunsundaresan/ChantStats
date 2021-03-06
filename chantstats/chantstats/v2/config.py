import os
from .repertoire_and_genre import RepertoireAndGenreType


class ChantStatsConfig:
    def __init__(self, musicxml_paths):
        self.musicxml_paths = {RepertoireAndGenreType(key): path for (key, path) in musicxml_paths.items()}

    def get_musicxml_path(self, repertoire_and_genre):
        rep_and_genre = RepertoireAndGenreType(repertoire_and_genre)
        musicxml_path = self.musicxml_paths[rep_and_genre]
        return musicxml_path

    @classmethod
    def from_env(cls):
        try:
            chants_dir = os.environ["CHANTS_DIR"]
        except KeyError:
            raise RuntimeError("The environment variable CHANTS_DIR must be defined to run the tests.")

        return cls(
            musicxml_paths={
                "plainchant_sequences": os.path.join(chants_dir, "BN_lat_1112_Sequences", "musicxml"),
                "responsorial_chants": os.path.join(chants_dir, "Organum_Chant_Files_MLO_II_III_IV", "musicxml"),
                "organum_pieces": os.path.join(chants_dir, "Organum_Files", "musicxml", "all"),
                "organum_phrases": os.path.join(chants_dir, "Organum_Files", "musicxml", "all"),
            }
        )
