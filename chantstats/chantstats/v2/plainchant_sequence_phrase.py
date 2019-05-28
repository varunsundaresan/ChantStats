import music21
import numpy as np
import pandas as pd
from music21.interval import Interval
from .ambitus import calculate_ambitus
from .mode_degree import ModeDegree
from .note_pair import NotePair
from .pitch_class import PC

__all__ = ["PlainchantSequencePhrase"]


def check_step_size(notes, allow_thirds, max_step_size=None):
    max_step_size = max_step_size or (4 if allow_thirds else 2)
    note_pairs = [NotePair(n1, n2) for n1, n2 in zip(notes, notes[1:])]
    return all([note_pair.semitones <= max_step_size for note_pair in note_pairs])


def has_framing_interval(notes, interval_name):
    return Interval(notes[0], notes[-1]).name == interval_name


class MelodicOutline:
    def __init__(self, notes):
        self.notes = notes
        self.framing_note_pair = NotePair(self.notes[0], self.notes[-1])
        self.framing_interval = self.framing_note_pair.interval
        assert self.framing_interval.name in ["P4", "P5"]
        self.bottom_pc = self.framing_note_pair.bottom_pc
        self.top_pc = self.framing_note_pair.top_pc

    def __repr__(self):
        return f"<MO: pcs{self.bottom_pc}^{self.top_pc}_M{self.framing_interval.name[-1]}, {[n.nameWithOctave for n in self.notes]}>"


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
        self._melodic_outline_candidates = self._calculate_melodic_outline_candidates_for_phrase()

    def __repr__(self):
        return f"<Phrase {self.phrase_number} of piece {self.piece}>"

    def _calculate_melodic_outline_candidates_for_phrase(self):
        directions = pd.Series([note_pair.direction for note_pair in self.note_pairs])
        directions_ffill = directions.replace(0, np.NaN).ffill(downcast="infer").bfill(downcast="infer")
        dir_changes = directions_ffill.diff().fillna(0, downcast="infer") != 0
        offsets_with_dir_changes = dir_changes[dir_changes != 0].index
        mo_slices = list(zip(offsets_with_dir_changes, offsets_with_dir_changes[1:]))
        mo_slices = (
            [(0, offsets_with_dir_changes[0])] + mo_slices + [(offsets_with_dir_changes[-1], len(self.notes) + 1)]
        )
        mo_slices = [slice(i, j + 1) for (i, j) in mo_slices]
        mo_candidates = [self.notes[sl] for sl in mo_slices]
        return mo_candidates

    def get_melodic_outlines(self, interval, *, allow_thirds=False):
        return [
            MelodicOutline(candidate)
            for candidate in self._melodic_outline_candidates
            if has_framing_interval(candidate, interval) and check_step_size(candidate, allow_thirds)
        ]
