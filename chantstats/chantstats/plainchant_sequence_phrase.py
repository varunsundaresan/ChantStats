import music21
import re

from .ambitus import calculate_ambitus
from .mode_degrees import calculate_mode_degrees
from .pitch_class_freqs import PCFreqs, ModeDegreeFreqs
from .pitch_class_tendencies import PCTendencies


class PlainchantSequencePhrase:
    """
    Represents a phrase in a plainchant sequence piece.
    """

    def __init__(self, measure_stream, *, piece):
        assert isinstance(measure_stream, music21.stream.Measure)
        self.piece = piece
        self.measure_stream = measure_stream
        self.phrase_number = self.measure_stream.number
        self.notes = self.measure_stream.notes
        self.lowest_note = min(self.notes)
        self.pitch_classes = [n.name for n in self.notes]
        self.phrase_final = self.pitch_classes[-1]
        self.final = self.phrase_final  # alias for consistency with other analysis items (e.g. pieces)
        self.note_of_phrase_final = self.notes[-1]
        self.note_of_final = self.note_of_phrase_final  # alias for consistency with other analysis items (e.g. pieces)
        self.phrase_final_note = self.notes[-1]
        self.mode_degrees = calculate_mode_degrees(self)
        self.time_signature = self.piece.stream.flat.getElementAtOrBefore(
            self.measure_stream.getOffsetInHierarchy(self.piece.stream), [music21.meter.TimeSignature]
        ).ratioString
        self.ambitus = calculate_ambitus(self)

    @property
    def pc_freqs(self):
        return PCFreqs(self.pitch_classes)

    @property
    def mode_degree_freqs(self):
        return ModeDegreeFreqs(self.mode_degrees)

    @property
    def pc_tendencies(self):
        return PCTendencies.from_pitch_classes(self.pitch_classes)

    def __repr__(self):
        return f"<Phrase {self.phrase_number} of piece {self.piece}>"

    @property
    def is_amen_formula(self):
        """
        Return True if the piece has an amen formula as the last phrase, where
        an amen formula is characterised by a 5/4 measure and the lyrics "Amen".
        """
        has_5_4_time_signature = "5/4" == self.time_signature

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
