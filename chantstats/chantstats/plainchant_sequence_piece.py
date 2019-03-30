import music21
import os
import re
from enum import Enum
from glob import glob
from music21.interval import Interval
from time import time
from tqdm import tqdm

from .logging import logger
from .plainchant_sequence_phrase import PlainchantSequencePhrase


class FrameType(str, Enum):
    """
    Possible frame types for pieces.
    """

    MONOMODAL_FRAME = "monomodal_frame"
    HEAVY_POLYMODAL_FRAME_1 = "heavy_polymodal_frame_1"
    HEAVY_POLYMODAL_FRAME_2 = "heavy_polymodal_frame_2"
    LIGHT_POLYMODAL_FRAME_1 = "light_polymodal_frame_1"
    LIGHT_POLYMODAL_FRAME_2 = "light_polymodal_frame_2"


class AmbitusType(str, Enum):
    """
    Possible ambitus types for pieces.
    """

    AUTHENTIC = "authentic"
    PLAGAL = "plagal"
    UNDEFINED = "undefined"


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
        self.note_of_main_final = self.note_of_first_phrase_final if not self.has_heavy_polymodal_frame else None
        # Note that non_modulatory_phrases will be empty if main_final is None
        self.non_modulatory_phrases = [p for p in self.phrases if p.phrase_final == self.main_final]
        self.ambitus = self._calculate_ambitus()

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

    def _calculate_ambitus(self):
        if self.main_final is None:
            return AmbitusType.UNDEFINED

        interval = Interval(self.note_of_main_final, self.lowest_note)
        if 0 >= interval.semitones >= -4:
            return AmbitusType.AUTHENTIC
        elif -5 >= interval.semitones > -12:
            return AmbitusType.PLAGAL
        else:
            raise Exception(  # pragma: no cover
                "Check the logic in the ambitus calculation! "
                "We expect the lowest note to be less than an octave "
                "below the main final. The chant being analysed was: "
                "'{}'".format(self.prettyname)
            )


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
