import music21
import os
import re
from enum import Enum

from .exceptions import UndefinedMainFinal
from .pitch_class_freqs import PCFreqs


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
        elif isinstance(stream_or_filename, music21.stream.Stream):
            self.stream = stream_or_filename
            self.filename_full = ""
            self.filename_short = ""
        else:
            raise TypeError(f"Cannot load piece from object of type: '{type(stream_or_filename)}'")

        num_parts = len(self.stream.parts)
        if num_parts != 1:
            raise ValueError(f"Piece must have exactly one tenor part. Found {num_parts} parts.")

        self.tenor = self.stream.parts[0]
        self.phrases = [PlainchantSequencePhrase(m, piece=self) for m in self.measures]
        self.num_phrases = len(self.phrases)
        self.phrase_finals = [p.phrase_final for p in self.phrases]
        self.first_phrase_final = self.phrase_finals[0]
        self.last_phrase_final = self.phrase_finals[-1]
        self.penultimate_phrase_final = self.phrase_finals[-2]
        self.antepenultimate_phrase_final = self.phrase_finals[-3]
        self.has_amen_formula = self.phrases[-1].is_amen_formula
        self.frame_type = self._calculate_frame_type()
        self.has_heavy_polymodal_frame = has_heavy_polymodal_frame(self)
        # self.main_final = self._calculate_main_final()

    def __repr__(self):
        return f"<Piece '{self.filename_short}'>"

    @property
    def pc_freqs(self):
        raise NotImplementedError(
            "This should probably not be implemented directly because we will want to "
            "filter pieces in different ways before calculating the PC frequencies!"
        )

    @property
    def measures(self):
        for measure in self.tenor.getElementsByClass("Measure"):
            yield measure

    def _calculate_frame_type(self):
        if self.first_phrase_final == self.last_phrase_final:
            # sanity check to ensure that amen formulas don't behave weirdly
            if self.has_amen_formula and self.first_phrase_final != self.penultimate_phrase_final:
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

    @property
    def main_final(self):
        if self.has_heavy_polymodal_frame:
            raise UndefinedMainFinal(f"Main final undefined for piece with heavey polymomdal frame: {self}")
        else:
            return self.first_phrase_final


class PlainchantSequencePhrase:
    """
    Represents a phrase in a plainchant sequence piece
    """

    def __init__(self, measure_stream, *, piece):
        assert isinstance(measure_stream, music21.stream.Measure)
        self.piece = piece
        self.measure_stream = measure_stream
        self.phrase_number = self.measure_stream.number
        self.notes = self.measure_stream.notes
        self.pitch_classes = [n.name for n in self.notes]
        self.phrase_final = self.pitch_classes[-1]
        self.pc_freqs = PCFreqs(self.pitch_classes)

    def __repr__(self):
        return f"<Phrase {self.phrase_number} of piece {self.piece}>"

    @property
    def is_amen_formula(self):
        try:
            has_5_4_time_signature = "5/4" == self.measure_stream.timeSignature.ratioString
        except AttributeError:  # pragma: no cover
            raise NotImplementedError(
                "TODO: some phrases do not have a time signature themselves. "
                "In this case we need to extract it from a previous measure."
            )

        lyric_searcher = music21.search.lyrics.LyricSearcher()
        regex_amen = re.compile("amen", re.IGNORECASE)
        amen_lyrics_search_result = lyric_searcher.search(regex_amen, s=self.measure_stream)
        has_amen_lyrics = [] != amen_lyrics_search_result

        # Sanity check, because we expect any 5/4 phrase to have the lyrics "Amen"
        if has_5_4_time_signature and not has_amen_lyrics:  # pragma: no cover
            raise RuntimeError(
                f"Phrase has a 5/4 time signature but no amen lyrics were found. "
                f"This is unexpected, please investigate. "
                f"Phrase where this occurred: {self}"
            )

        return has_5_4_time_signature and has_amen_lyrics
