import numpy as np
import pandas as pd
from .note_pair import NotePair

__all__ = ["calculate_melodic_outlines"]


def is_melodic_outline(notes, interval, steps_only=True):
    note_pairs = [NotePair(n1, n2) for n1, n2 in zip(notes, notes[1:])]
    if steps_only:
        contains_no_leaps = all([note_pair.semitones <= 2 for note_pair in note_pairs])
    else:
        contains_no_leaps = True

    is_expected_interval = NotePair(notes[0], notes[-1]).interval.name == interval

    return contains_no_leaps and is_expected_interval


def calculate_melodic_outlines(notes, interval, steps_only=True):
    note_pairs = [NotePair(n1, n2) for n1, n2 in zip(notes, notes[1:])]
    directions = pd.Series([note_pair.direction for note_pair in note_pairs])
    directions_ffill = directions.replace(0, np.NaN).ffill(downcast="infer").bfill(downcast="infer")
    dir_changes = directions_ffill.diff().fillna(0, downcast="infer") != 0
    offsets_with_dir_changes = dir_changes[dir_changes != 0].index
    mo_slices = list(zip(offsets_with_dir_changes, offsets_with_dir_changes[1:]))
    mo_slices = [(0, offsets_with_dir_changes[0])] + mo_slices + [(offsets_with_dir_changes[-1], len(notes) + 1)]
    mo_slices = [slice(i, j + 1) for (i, j) in mo_slices]
    mo_candidates = [notes[sl] for sl in mo_slices]
    return [c for c in mo_candidates if is_melodic_outline(c, interval, steps_only=steps_only)]
