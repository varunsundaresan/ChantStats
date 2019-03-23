from .context import chantstats
from chantstats import PhraseCollection

from .sample_pieces import *


def test_phrase_collection_num_phrases():
    pcoll = PhraseCollection(piece1.phrases)
    assert pcoll.num_phrases == 12

    pcoll = PhraseCollection(piece2.phrases)
    assert pcoll.num_phrases == 14


def test_phrase_collection_pc_freqs():
    pcoll = PhraseCollection(piece1.phrases)
    assert pcoll.num_phrases == 12
    assert list(pcoll.pc_freqs.abs_freqs) == [41, 0, 50, 22, 34, 18, 2, 29]

    pcoll = PhraseCollection(piece2.phrases)
    assert pcoll.num_phrases == 14
    assert list(pcoll.pc_freqs.abs_freqs) == [21, 0, 8, 29, 60, 34, 25, 23]
