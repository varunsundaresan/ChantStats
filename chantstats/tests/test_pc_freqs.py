from .context import chantstats
from chantstats.pitch_class_freqs import PCFreqs


def test_absolute_pc_freqs():
    pcs = ["A", "C", "C", "D", "C", "D", "G"]
    pc_freqs = PCFreqs(pcs)
    assert list(pc_freqs.abs_freqs.index) == ["A", "B-", "B", "C", "D", "E", "F", "G"]
    assert list(pc_freqs.abs_freqs) == [1, 0, 0, 3, 2, 0, 0, 1]

    pcs = ["F", "C", "B-", "G", "F"]
    pc_freqs = PCFreqs(pcs)
    assert list(pc_freqs.abs_freqs.index) == ["A", "B-", "B", "C", "D", "E", "F", "G"]
    assert list(pc_freqs.abs_freqs) == [0, 1, 0, 1, 0, 0, 2, 1]


def test_relative_pc_freqs():
    pcs = ["A", "C", "C", "D", "C", "D", "G", "C"]
    pc_freqs = PCFreqs(pcs)
    assert list(pc_freqs.rel_freqs.index) == ["A", "B-", "B", "C", "D", "E", "F", "G"]
    assert list(pc_freqs.rel_freqs) == [12.5, 0, 0, 50.0, 25.0, 0, 0, 12.5]

    pcs = ["F", "C", "B-", "G", "F"]
    pc_freqs = PCFreqs(pcs)
    assert list(pc_freqs.rel_freqs.index) == ["A", "B-", "B", "C", "D", "E", "F", "G"]
    assert list(pc_freqs.rel_freqs) == [0, 20.0, 0, 20.0, 0, 0, 40.0, 20.0]
