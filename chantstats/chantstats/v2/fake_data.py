import numpy as np
from music21.note import Note
from .pitch_class import PC
from .mode_degree import ModeDegree
from .note_pair import NotePair
from .plainchant_sequence_piece import PlainchantSequencePiece

__all__ = ["make_random_notes", "FakePhrase"]

candidate_notes = [
    Note("D3"),
    Note("E3"),
    Note("F3"),
    Note("G3"),
    Note("A3"),
    Note("B3"),
    Note("C4"),
    Note("D4"),
    Note("E4"),
    Note("F4"),
    Note("G4"),
    Note("A4"),
    Note("B4"),
]


def make_random_notes(num, seed):
    np.random.seed(seed)
    return list(np.random.choice(candidate_notes, size=num))


class FakePhrase:
    def __init__(self, *, phrase_number, seed, phrase_length=None):
        self.randgen = np.random.RandomState(seed=seed)
        self.phrase_number = phrase_number
        self.phrase_length = phrase_length or int(self.randgen.normal(loc=24.5, scale=8.8))
        self.notes = make_random_notes(self.phrase_length, seed=self.phrase_number)
        self.pitch_classes = [PC.from_note(n) for n in self.notes]
        self.note_of_final = self.notes[-1]
        self.phrase_final = self.pitch_classes[-1]
        self.final = self.phrase_final  # alias
        self.lowest_note = min(self.notes)

        self.pc_pairs = list(zip(self.pitch_classes, self.pitch_classes[1:]))
        self.mode_degrees = [ModeDegree.from_note_pair(note=n, base_note=self.note_of_final) for n in self.notes]
        self.note_pairs = [NotePair(n1, n2) for (n1, n2) in zip(self.notes, self.notes[1:])]
        self.mode_degree_pairs = list(zip(self.mode_degrees, self.mode_degrees[1:]))


class FakePiece(PlainchantSequencePiece):
    def __init__(self, *, piece_number, seed=None):
        seed = seed or piece_number
        self.randgen = np.random.RandomState()
        self.randgen.seed(seed)

        self.number = piece_number
        self.num_phrases = int(self.randgen.normal(loc=19, scale=6.1))
        self.phrases = [FakePhrase(phrase_number=i, seed=(self.number, i)) for i in range(self.num_phrases)]

        self.filename_short = f"FakePiece_{self.number:02d}.xml"

    def __repr__(self):
        return f"<FakePiece: idx={self.number}>"
