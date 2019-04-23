from itertools import groupby
from operator import itemgetter

from .ambitus import calculate_ambitus
from .pitch_class_freqs import PCFreqs

__all__ = ["MonomodalSection", "extract_monomodal_sections"]


class MonomodalSection:
    """
    Represents a section of consecutive phrases in a given piece with the same phrase-final.
    """

    def __init__(self, piece, idx_start, idx_end):
        assert piece.__class__.__name__ == "PlainchantSequencePiece"
        self.piece = piece
        self.idx_start = idx_start
        self.idx_end = idx_end
        self.phrases = piece.phrases[idx_start - 1 : idx_end]
        self.length = len(self.phrases)
        if len(set(p.phrase_final for p in self.phrases)) != 1:
            error_msg = (
                f"Non-unique phrase final: {set(p.phrase_final for p in self.phrases)}"
                f"(section: {self.idx_start}-{self.idx_end})"
            )
            raise ValueError(error_msg)
        self.final = self.phrases[0].phrase_final
        assert all([p.final == self.final for p in self.phrases])  # sanity check
        self.descr = f"s{self.piece.number:02d}.{self.final}.mm_{self.idx_start:02d}_{self.idx_end:02d}"
        self.note_of_final = self.phrases[0].notes[-1]
        self.lowest_note = min([p.lowest_note for p in self.phrases])
        self.ambitus = calculate_ambitus(self)

    def __repr__(self):
        s = (
            f"<MonomodalSection: '{self.piece.filename_short}', "
            f"phrase-final '{self.final}', "
            f"phrases {self.idx_start}-{self.idx_end} "
            f"(length {len(self)}), "
            f"ambitus={self.ambitus.value!r}>"
        )
        return s

    def __len__(self):
        return len(self.phrases)

    @property
    def pc_freqs(self):
        return sum([p.pc_freqs for p in self.phrases], PCFreqs.zero_freqs)


def extract_monomodal_sections(piece, *, enforce_same_ambitus, min_length=3):
    """
    Extract monomodal sections (= sections of consecutive phrases with the same phrase-final).

    Parameters
    ----------
    piece : PlainchantSequencePiece
        The piece from which to extract monomodal sections.
    ignore_ambitus : boolean
        If True, all phrases in the monomodal section must have
        the same ambitus (in addition to the same phrase-final).
    min_length : int
        Minimum length for a section to be included in the result
        (any phrase sections with fewer phrases are discarded).

    Returns
    -------
    list of MonomodalSection
    """
    if enforce_same_ambitus:
        key_func = lambda phrase: (phrase.final, phrase.ambitus)
    else:
        key_func = lambda phrase: phrase.final

    get_idx_start = lambda grp: grp[1][0][0]
    get_idx_end = lambda grp: grp[1][-1][0]

    items = [key_func(p) for p in piece.phrases]
    grps = [(x, list(grp)) for x, grp in groupby(enumerate(items, start=1), key=itemgetter(1))]
    monomodal_sections = [MonomodalSection(piece, get_idx_start(g), get_idx_end(g)) for g in grps]
    return [x for x in monomodal_sections if len(x) >= min_length]
