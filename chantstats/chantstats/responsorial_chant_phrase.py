import music21
from .ambitus import calculate_ambitus
from .mode_degrees import calculate_mode_degrees
from .pitch_class_freqs import PCFreqs, ModeDegreeFreqs
from .pitch_class_tendencies import PCTendencies

__all__ = ["ResponsorialChantPhrase"]


class ResponsorialChantPhrase:
    """
    Represents a phrase in a responsorial chant piece.
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
