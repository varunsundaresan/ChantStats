import music21
import os
import re
from functools import lru_cache
from glob import glob
from time import time
from tqdm import tqdm
from ..logging import logger
from ..repertoire_and_genre import RepertoireAndGenreType
from .responsorial_chant_phrase import ResponsorialChantPhrase
from .responsorial_chant_stanza import ResponsorialChantStanza
from ..analysis_functions import (
    calculate_L5_occurrences,
    calculate_L4_occurrences,
    calculate_M5_occurrences,
    calculate_M4_occurrences,
)

__all__ = ["ResponsorialChantPiece"]


class ResponsorialChantPiece:
    def __init__(self, stream_or_filename):
        if isinstance(stream_or_filename, str):
            self.stream = music21.converter.parse(stream_or_filename)
            self.filename_full = os.path.abspath(stream_or_filename)
            self.filename_short = os.path.basename(stream_or_filename)
        # elif isinstance(stream_or_filename, music21.stream.Stream):
        #     self.stream = stream_or_filename
        #     self.filename_full = ""
        #     self.filename_short = ""
        else:  # pragma: no cover
            raise TypeError(f"Cannot load piece from object of type: '{type(stream_or_filename)}'")

        # TODO: extract stub_descr from filename
        self.descr_stub = re.match("^(F3[MO]\d\dps).*\.xml$", self.filename_short).group(1)

        num_parts = len(self.stream.parts)
        if num_parts != 1:  # pragma: no cover
            raise ValueError(f"Piece must have exactly one tenor part. Found {num_parts} parts.")

        self.tenor = self.stream.parts[0]

        # TODO: should we actually extract phrases here if we might drop them later?!
        self.measures = list(self.tenor.getElementsByClass("Measure"))
        self.phrases = [ResponsorialChantPhrase(m, piece=self) for m in self.measures]
        self.num_phrases = len(self.phrases)

    def __repr__(self):
        return f"<Piece '{self.filename_short}'>"

    def get_stanzas(self):
        stanza_ends = [p.phrase_number for p in self.phrases if p.is_last_phrase_in_stanza]
        stanza_starts = [1] + [n + 1 for n in stanza_ends[:-1]]
        idx_of_last_phrase_in_piece = self.phrases[-1].phrase_number
        assert idx_of_last_phrase_in_piece in stanza_ends
        return [
            ResponsorialChantStanza(self, idx_start, idx_end)
            for (idx_start, idx_end) in zip(stanza_starts, stanza_ends)
        ]

    def get_stanzas_without_modulatory_phrases(self):
        return [s.without_modulatory_phrases() for s in self.get_stanzas()]

    def get_occurring_mode_degrees(self):
        mds = set()
        for phrase in self.phrases:
            mds.update(phrase.mode_degrees)
        return mds


@lru_cache(maxsize=10)
def load_responsorial_chant_pieces(input_dir, *, pattern="*.xml"):
    """
    Load responsorial chant pieces from MusicXML files in a given input directory.

    Parameters
    ----------
    input_dir : str
        Input directory in which to look for MusicXML files.
    pattern : str, optional
        Filename pattern; this can be used to filter the files
        to be loaded to a subset (for example during testing).

    Returns
    -------
    list of ResponsorialChantPiece
    """
    pattern = pattern if pattern is not None else "*.xml"
    filenames = sorted(glob(os.path.join(input_dir, pattern)))
    logger.debug(f"Found {len(filenames)} pieces matching the pattern '{pattern}'.")
    logger.debug(f"Loading pieces... ")
    tic = time()
    pieces = [ResponsorialChantPiece(f) for f in tqdm(filenames)]
    toc = time()
    logger.debug(f"Done. Loaded {len(pieces)} pieces.")
    logger.debug(f"Loading pieces took {toc-tic:.2f} seconds.")
    return pieces


class ResponsorialChantPieces:
    def __init__(self, pieces):
        assert all([isinstance(p, ResponsorialChantPiece) for p in pieces])
        self.pieces = pieces
        self.repertoire_and_genre = RepertoireAndGenreType("responsorial_chants")

    def __repr__(self):
        return f"<Collection of {len(self.pieces)} plainchant sequence pieces>"

    def __getitem__(self, idx):
        return self.pieces[idx]

    def __iter__(self):
        yield from self.pieces

    @classmethod
    def from_musicxml_files(cls, cfg, filename_pattern=None):
        musicxml_path = cfg.get_musicxml_path("responsorial_chants")
        pieces = load_responsorial_chant_pieces(musicxml_path, pattern=filename_pattern)
        return cls(pieces)

    def get_analysis_inputs(
        self, mode=None, min_num_phrases_per_monomodal_section=None, min_num_notes_per_monomodal_section=None
    ):
        return sum([piece.get_stanzas_without_modulatory_phrases() for piece in self.pieces], [])

    def get_occurring_mode_degrees(self):
        mds = set()
        for piece in self.pieces:
            mds.update(piece.get_occurring_mode_degrees())
        return mds

    def get_L_and_M_occurrences(self, which, unit):
        res = set()
        if which == "L5M5":
            res.update(self._get_L_or_M_occurrences("L5", unit))
            res.update(self._get_L_or_M_occurrences("M5", unit))
        elif which == "L4M4":
            res.update(self._get_L_or_M_occurrences("L4", unit))
            res.update(self._get_L_or_M_occurrences("M4", unit))
        else:
            raise NotImplementedError()
        return res

    def _get_L_or_M_occurrences(self, which, unit):
        funcs = {
            "L5": calculate_L5_occurrences,
            "L4": calculate_L4_occurrences,
            "M5": calculate_M5_occurrences,
            "M4": calculate_M4_occurrences,
        }
        res = set()
        for piece in self.pieces:
            res.update(set(sum([funcs[which](phrase, unit=unit) for phrase in piece.phrases], [])))
        return res
