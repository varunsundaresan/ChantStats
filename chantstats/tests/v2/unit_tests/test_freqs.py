import pandas as pd
import pytest
from numpy import NaN
from pandas.util.testing import assert_series_equal
from music21.note import Note
from .context import chantstats
from chantstats.v2.freqs import PCFreqs
from chantstats.v2.pitch_class import PC


OCCURRING_PCS = ["D", "E-", "E", "F", "F#", "G", "A", "B-", "B", "C"]
assert OCCURRING_PCS == PC.allowed_values


def test_pc_freqs():
    notes = [Note("A3"), Note("G3"), Note("A3"), Note("C3"), Note("D3"), Note("C3"), Note("A3"), Note("B-3")]
    pc_freqs = PCFreqs.from_notes(notes)
    abs_freqs_expected = pd.Series([1, 0, 0, 0, 0, 1, 3, 1, 0, 2], index=OCCURRING_PCS)
    rel_freqs_expected = pd.Series([12.5, 0, 0, 0, 0, 12.5, 37.5, 12.5, 0, 25.0], index=OCCURRING_PCS)
    assert_series_equal(abs_freqs_expected, pc_freqs.abs_freqs)
    assert_series_equal(rel_freqs_expected, pc_freqs.rel_freqs)


def test_zero_pc_freqs():
    zero_abs_freqs_expected = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], index=OCCURRING_PCS, dtype=int)
    zero_rel_freqs_expected = pd.Series(
        [NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN], index=OCCURRING_PCS, dtype=float
    )
    assert_series_equal(zero_abs_freqs_expected, PCFreqs.zero_freqs.abs_freqs)
    assert_series_equal(zero_rel_freqs_expected, PCFreqs.zero_freqs.rel_freqs)


def test_invalid_values():
    with pytest.raises(ValueError, match="Unexpected values: .* Must be a subset of allowed values"):
        PCFreqs(["Z"])


def test_add_pc_freqs():
    pc_freqs_1 = PCFreqs(["A", "C", "C", "E"])
    pc_freqs_2 = PCFreqs(["A", "D", "B-", "C", "C", "A"])
    pc_freqs_sum = pc_freqs_1 + pc_freqs_2
    pc_freqs_sum_expected = PCFreqs(pd.Series([1, 0, 1, 0, 0, 0, 3, 1, 0, 4], index=OCCURRING_PCS))
    assert_series_equal(pc_freqs_sum_expected.abs_freqs, pc_freqs_sum.abs_freqs)
