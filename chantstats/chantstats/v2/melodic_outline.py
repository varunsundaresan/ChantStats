import numpy as np
import pandas as pd
from music21.interval import Interval
from .note_pair import NotePair

__all__ = ["MelodicOutline", "has_framing_interval", "check_step_size"]


def calculate_melodic_outline_candidates_for_phrase(phrase):
    """
    Parameters
    ----------
    phrase
        A phrase in a plainchant sequence or responsorial chant piece.
        Must have the attributes `notes` and `note_pairs`.
    """
    directions = pd.Series([note_pair.direction for note_pair in phrase.note_pairs])
    directions_ffill = directions.replace(0, np.NaN).ffill(downcast="infer").bfill(downcast="infer")
    dir_changes = directions_ffill.diff().fillna(0, downcast="infer") != 0
    offsets_with_dir_changes = dir_changes[dir_changes != 0].index
    mo_slices = list(zip(offsets_with_dir_changes, offsets_with_dir_changes[1:]))
    mo_slices = [(0, offsets_with_dir_changes[0])] + mo_slices + [(offsets_with_dir_changes[-1], len(phrase.notes) + 1)]
    mo_slices = [slice(i, j + 1) for (i, j) in mo_slices]
    mo_candidates = [phrase.notes[sl] for sl in mo_slices]
    return mo_candidates


def get_melodic_outlines_from_candidates(melodic_outline_candidates, interval_name, *, allow_thirds=False):
    """
    Parameters
    ----------
    melodic_outline_candidates
        List containing lists of notes, each of which represents a melodic outline candidate.
    """
    return [
        MelodicOutline(notes)
        for notes in melodic_outline_candidates
        if has_framing_interval(notes, interval_name) and check_step_size(notes, allow_thirds)
    ]


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
