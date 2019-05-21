import music21
from .ambitus import calculate_ambitus
from .pitch_class import PC

__all__ = ["PlainchantSequencePhrase"]


class PlainchantSequencePhrase:
    """
    Represents a phrase in a plainchant sequence piece.
    """

    def __init__(self, measure_stream, *, piece):
        assert isinstance(measure_stream, music21.stream.Measure)
        self.piece = piece
        self.measure_stream = measure_stream
        self.phrase_number = self.measure_stream.number
        self.notes = list(self.measure_stream.notes)
        self.lowest_note = min(self.notes)
        self.note_of_phrase_final = self.notes[-1]
        self.note_of_final = self.note_of_phrase_final  # alias for consistency with other analysis items (e.g. pieces)
        self.phrase_final = PC.from_note(self.note_of_phrase_final)
        self.final = self.phrase_final  # alias for consistency with other analysis items (e.g. pieces)
        self.ambitus = calculate_ambitus(self)

    def __repr__(self):
        return f"<Phrase {self.phrase_number} of piece {self.piece}>"
