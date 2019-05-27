import music21
from .ambitus import calculate_ambitus
from .mode_degree import ModeDegree
from .note_pair import NotePair
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

        self.pitch_classes = [PC.from_note(n) for n in self.notes]
        self.mode_degrees = [ModeDegree.from_note_pair(note=n, base_note=self.note_of_final) for n in self.notes]
        self.pc_pairs = list(zip(self.pitch_classes, self.pitch_classes[1:]))
        self.note_pairs = [NotePair(n1, n2) for (n1, n2) in zip(self.notes, self.notes[1:])]
        self.mode_degree_pairs = list(zip(self.mode_degrees, self.mode_degrees[1:]))

    def __repr__(self):
        return f"<Phrase {self.phrase_number} of piece {self.piece}>"
