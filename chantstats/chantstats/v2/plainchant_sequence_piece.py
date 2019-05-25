import music21
import os
import re
from functools import lru_cache
from glob import glob
from time import time
from tqdm import tqdm

from .logging import logger
from .modal_category import ModalCategoryType
from .plainchant_sequence_phrase import PlainchantSequencePhrase
from .plainchant_sequence_monomodal_section import extract_monomodal_sections_from_piece, extract_monomodal_sections
from .repertoire_and_genre import RepertoireAndGenreType


class PlainchantSequencePiece:
    """
    Represents a plainchant sequence piece.
    """

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

        self.name = re.sub(
            r"\.xml$", "", re.sub("_", " ", self.filename_short)
        )  # remove .xml suffix and replace underscores with spaces
        self.number = int(re.match(r"^BN_lat_1112_Sequence_([0-9][0-9])_.*\.xml", self.filename_short).group(1))

        num_parts = len(self.stream.parts)
        if num_parts != 1:  # pragma: no cover
            raise ValueError(f"Piece must have exactly one tenor part. Found {num_parts} parts.")

        self.tenor = self.stream.parts[0]
        self.measures = list(self.tenor.getElementsByClass("Measure"))
        self.phrases = [PlainchantSequencePhrase(m, piece=self) for m in self.measures]
        self.num_phrases = len(self.phrases)

    def __repr__(self):
        return f"<Piece '{self.filename_short}'>"

    def get_monomodal_sections(self, *, enforce_same_phrase_ambitus, min_num_phrases=3, min_num_notes=80):
        """
        Extract monomodal sections (= sections of consecutive phrases
        with the same phrase-final, and optionally the same ambitus).

        Parameters
        ----------
        piece : PlainchantSequencePiece
            The piece from which to extract monomodal sections.
        enforce_same_phrase_ambitus: boolean
            If True, all phrases in the monomodal section must have
            the same ambitus (in addition to the same phrase-final).
        min_num_phrases : int
            Minimum number of phrases for a section to be included in the
            result (any phrase sections with fewer phrases are discarded).
        min_num_notes : int
            Minimum number of notes for a section to be included in the
            result (any phrase sections with fewer notes are discarded).

        Returns
        -------
        list of MonomodalSection
        """
        return extract_monomodal_sections_from_piece(
            self,
            enforce_same_phrase_ambitus=enforce_same_phrase_ambitus,
            min_num_phrases=min_num_phrases,
            min_num_notes=min_num_notes,
        )


@lru_cache(maxsize=10)
def load_plainchant_sequence_pieces(input_dir, *, pattern="*.xml", exclude_heavy_polymodal_frame_pieces=False):
    """
    Load plainchant sequence pieces from MusicXML files in a given input directory.

    Parameters
    ----------
    input_dir : str
        Input directory in which to look for MusicXML files.
    pattern : str, optional
        Filename pattern; this can be used to filter the files
        to be loaded to a subset (for example during testing).
    exclude_heavy_polymodal_frame_pieces : bool
        If True, exclude pieces which have heavy polymodal frame
        (and as a result don't have a well-defined main final).

    Returns
    -------
    list of PlainchantSequencePiece
    """
    pattern = pattern if pattern is not None else "*.xml"
    filenames = sorted(glob(os.path.join(input_dir, pattern)))
    logger.debug(f"Found {len(filenames)} pieces matching the pattern '{pattern}'.")
    logger.debug(f"Loading pieces... ")
    tic = time()
    pieces = [PlainchantSequencePiece(f) for f in tqdm(filenames)]
    if exclude_heavy_polymodal_frame_pieces:
        # pieces = [p for p in pieces if not p.has_heavy_polymodal_frame]
        raise NotImplementedError()
    toc = time()
    logger.debug(
        f"Done. Loaded {len(pieces)} pieces{' without heavy polymodal frames' if exclude_heavy_polymodal_frame_pieces else ''}."
    )
    logger.debug(f"Loading pieces took {toc-tic:.2f} seconds.")
    return pieces


class PlainchantSequencePieces:
    def __init__(self, pieces):
        assert all([isinstance(p, PlainchantSequencePiece) for p in pieces])
        self.pieces = pieces
        self.repertoire_and_genre = RepertoireAndGenreType("plainchant_sequences")

    def __repr__(self):
        return f"<Collection of {len(self.pieces)} plainchant sequence pieces>"

    def __getitem__(self, idx):
        return self.pieces[idx]

    def __iter__(self):
        yield from self.pieces

    @classmethod
    def from_musicxml_files(cls, cfg, filename_pattern=None):
        musicxml_path = cfg.get_musicxml_path("plainchant_sequences")
        pieces = load_plainchant_sequence_pieces(musicxml_path, pattern=filename_pattern)
        return cls(pieces)

    def get_analysis_inputs(
        self, mode, min_num_phrases_per_monomodal_section=3, min_num_notes_per_monomodal_section=80
    ):
        mode = ModalCategoryType(mode)
        return extract_monomodal_sections(
            self.pieces,
            enforce_same_phrase_ambitus=mode.enforce_same_ambitus,
            min_num_phrases=min_num_phrases_per_monomodal_section,
            min_num_notes=min_num_notes_per_monomodal_section,
        )


def load_pieces(repertoire_and_genre, cfg, filename_pattern=None):
    if repertoire_and_genre == "plainchant_sequences":
        return PlainchantSequencePieces.from_musicxml_files(cfg, filename_pattern=filename_pattern)
    else:
        raise NotImplementedError()
