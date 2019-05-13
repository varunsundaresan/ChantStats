import music21
import os
import re
from enum import Enum
from functools import lru_cache
from glob import glob
from time import time
from tqdm import tqdm

from .ambitus import get_ambitus
from .analysis_spec import RepertoireAndGenreType
from .logging import logger
from .modal_category import ModalCategoryType
from .plainchant_sequence_phrase import PlainchantSequencePhrase
from .plainchant_sequence_monomodal_sections import extract_monomodal_sections_from_piece, extract_monomodal_sections


class FrameType(str, Enum):
    """
    Possible frame types for pieces.
    """

    MONOMODAL_FRAME = "monomodal_frame"
    HEAVY_POLYMODAL_FRAME_1 = "heavy_polymodal_frame_1"
    HEAVY_POLYMODAL_FRAME_2 = "heavy_polymodal_frame_2"
    LIGHT_POLYMODAL_FRAME_1 = "light_polymodal_frame_1"
    LIGHT_POLYMODAL_FRAME_2 = "light_polymodal_frame_2"


def has_heavy_polymodal_frame(piece):
    return piece.frame_type in [FrameType.HEAVY_POLYMODAL_FRAME_1, FrameType.HEAVY_POLYMODAL_FRAME_2]


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
        )  # remove .xml suffix; replace underscores with spaces
        self.number = int(re.match(r"^BN_lat_1112_Sequence_([0-9][0-9])_.*\.xml", self.filename_short).group(1))

        num_parts = len(self.stream.parts)
        if num_parts != 1:  # pragma: no cover
            raise ValueError(f"Piece must have exactly one tenor part. Found {num_parts} parts.")

        self.tenor = self.stream.parts[0]
        self.phrases = [PlainchantSequencePhrase(m, piece=self) for m in self.measures]
        self.num_phrases = len(self.phrases)
        self.phrase_finals = [p.phrase_final for p in self.phrases]
        self.phrase_final_notes = [p.phrase_final_note for p in self.phrases]
        self.first_phrase_final = self.phrase_finals[0]
        self.note_of_first_phrase_final = self.phrase_final_notes[0]
        self.lowest_note = min([p.lowest_note for p in self.phrases])
        self.last_phrase_final = self.phrase_finals[-1]
        self.penultimate_phrase_final = self.phrase_finals[-2]
        self.antepenultimate_phrase_final = self.phrase_finals[-3]
        self.has_amen_formula = self.phrases[-1].is_amen_formula
        self.frame_type = self._calculate_frame_type()
        self.has_heavy_polymodal_frame = has_heavy_polymodal_frame(self)
        self.main_final = self.first_phrase_final if not self.has_heavy_polymodal_frame else None
        self.final = self.main_final  # alias for consistency with other analysis items (e.g.phrases)
        self.note_of_main_final = self.note_of_first_phrase_final if not self.has_heavy_polymodal_frame else None
        self.note_of_final = self.note_of_main_final  # alias for consistency with other analysis items (e.g. phrases)
        # Note that non_modulatory_phrases will be empty if main_final is None
        self.non_modulatory_phrases = [p for p in self.phrases if p.phrase_final == self.main_final]
        self.ambitus = get_ambitus(note_of_final=self.note_of_main_final, lowest_note=self.lowest_note)

    def __repr__(self):
        return f"<Piece '{self.filename_short}'>"

    @property
    def pc_freqs(self):  # pragma: no cover
        raise NotImplementedError(
            "The .pc_freqs attribute is not supported directly because different analyses "
            "require different pre-processing of pieces (such as omitting modulatory phrases). "
            "Therefore this pre-processing should be done first and only then should the "
            "PC frequencies be calculated."
        )

    @property
    def measures(self):
        for measure in self.tenor.getElementsByClass("Measure"):
            yield measure

    def _calculate_frame_type(self):
        if self.first_phrase_final == self.last_phrase_final:
            # sanity check to ensure that amen formulas don't behave weirdly
            if self.has_amen_formula and self.first_phrase_final != self.penultimate_phrase_final:  # pragma: no cover
                raise RuntimeError(
                    f"Piece seems to have a monomodal frame because the first and last phrase-final are the same. "
                    f"However, the last phrase is an amen formula and the penultimate phrase-final is different. "
                    f"What should we do in this case?"
                    f"Piece where this occurred: {self}"
                )

            return FrameType.MONOMODAL_FRAME
        else:
            if not self.has_amen_formula:
                return FrameType.HEAVY_POLYMODAL_FRAME_1
            else:
                if self.first_phrase_final == self.penultimate_phrase_final:
                    return FrameType.LIGHT_POLYMODAL_FRAME_1
                elif self.first_phrase_final == self.antepenultimate_phrase_final:
                    return FrameType.LIGHT_POLYMODAL_FRAME_2
                else:
                    return FrameType.HEAVY_POLYMODAL_FRAME_2

    def get_monomodal_sections(self, *, enforce_same_ambitus, min_length=3):
        """
        Extract monomodal sections (= sections of consecutive phrases
        with the same phrase-final, and optionally the same ambitus).

        Parameters
        ----------
        piece : PlainchantSequencePiece
            The piece from which to extract monomodal sections.
        enforce_same_ambitus: boolean
            If True, all phrases in the monomodal section must have
            the same ambitus (in addition to the same phrase-final).
        min_length : int
            Minimum length for a section to be included in the result
            (any phrase sections with fewer phrases are discarded).

        Returns
        -------
        list of MonomodalSection
        """
        return extract_monomodal_sections_from_piece(
            self, enforce_same_ambitus=enforce_same_ambitus, min_length=min_length
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
        pieces = [p for p in pieces if not p.has_heavy_polymodal_frame]
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

    @classmethod
    def from_musicxml_files(cls, cfg, filename_pattern=None):
        musicxml_path = cfg.get_musicxml_path("plainchant_sequences")
        pieces = load_plainchant_sequence_pieces(musicxml_path, pattern=filename_pattern)
        return cls(pieces)

    def get_analysis_inputs(self, mode, min_length_monomodal_sections=3):
        mode = ModalCategoryType(mode)
        return extract_monomodal_sections(
            self.pieces, enforce_same_ambitus=mode.enforce_same_ambitus, min_length=min_length_monomodal_sections
        )


def load_pieces(repertoire_and_genre, cfg, filename_pattern=None):
    if repertoire_and_genre == "plainchant_sequences":
        return PlainchantSequencePieces.from_musicxml_files(cfg, filename_pattern=filename_pattern)
    else:
        raise NotImplementedError()
