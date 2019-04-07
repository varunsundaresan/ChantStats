from itertools import groupby
from operator import itemgetter

from .pitch_class_freqs import PCFreqs

__all__ = ["MonomodalSection", "extract_phrase_stretches"]


class MonomodalSection:
    """
    Represents a stretch of consecutive phrases with the same phrase-final in a given piece.
    """

    def __init__(self, piece, idx_start, idx_end):
        self.piece = piece
        self.idx_start = idx_start
        self.idx_end = idx_end
        self.phrases = piece.phrases[idx_start - 1 : idx_end]
        self.length = len(self.phrases)
        if len(set(p.phrase_final for p in self.phrases)) != 1:
            error_msg = (
                f"Non-unique phrase final: {set(p.phrase_final for p in self.phrases)}"
                f"(stretch: {self.idx_start}-{self.idx_end})"
            )
            raise ValueError(error_msg)
        self.phrase_final = self.phrases[0].phrase_final
        self.descr = f"s{self.piece.number:02d}.{self.phrase_final}.mm_{self.idx_start:02d}_{self.idx_end:02d}"

    def __repr__(self):
        s = (
            f"<MonomodalSection: '{self.piece.filename_short}', "
            f"phrase-final '{self.phrase_final}', "
            f"phrases {self.idx_start}-{self.idx_end} "
            f"(length {len(self)})>"
        )
        return s

    def __len__(self):
        return len(self.phrases)

    @property
    def pc_freqs(self):
        return sum([p.pc_freqs for p in self.phrases], PCFreqs.zero_freqs)


class PhraseStretchInfo:
    def __init__(self, phrase_final, length, idx_start, idx_end):
        self.phrase_final = phrase_final
        self.length = length
        self.idx_start = idx_start
        self.idx_end = idx_end

    def __repr__(self):
        return f"<PhraseGroupInfo: '{self.phrase_final}', length={self.length} ({self.idx_start}-{self.idx_end})>"


def get_groups_with_length_and_indices(items):
    grps = [(x, list(grp)) for x, grp in groupby(enumerate(items, start=1), key=itemgetter(1))]
    grps = [PhraseStretchInfo(x, len(grp), grp[0][0], grp[-1][0]) for x, grp in grps]
    return grps


def extract_phrase_stretches(piece, *, min_length=3):
    """
    Extract stretches of consecutive phrases with the same phrase-final.

    Parameters
    ----------
    piece : PlainchantSequencePiece
        The piece from which to extract phrase stretches.
    min_length : int
        Minimum length for phrase stretches to be included in the result
        (any phrase stretches with fewer phrases are discarded).

    Returns
    -------
    list of MonomodalSection
    """
    grps = get_groups_with_length_and_indices(piece.phrase_finals)
    phrase_stretches = [MonomodalSection(piece, g.idx_start, g.idx_end) for g in grps]
    return [x for x in phrase_stretches if len(x) >= min_length]
