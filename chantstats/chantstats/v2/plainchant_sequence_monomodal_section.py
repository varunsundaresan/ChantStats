from itertools import groupby
from operator import itemgetter


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

    def __len__(self):
        return len(self.phrases)


def extract_monomodal_sections_from_piece(piece, *, enforce_same_ambitus, min_length=3):
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
        key_func = lambda phrase: (phrase.note_of_final, phrase.ambitus)
    else:
        key_func = lambda phrase: phrase.note_of_final

    get_idx_start = lambda grp: grp[1][0][0]
    get_idx_end = lambda grp: grp[1][-1][0]

    items = [key_func(p) for p in piece.phrases]
    grps = [(x, list(grp)) for x, grp in groupby(enumerate(items, start=1), key=itemgetter(1))]
    monomodal_sections = [MonomodalSection(piece, get_idx_start(g), get_idx_end(g)) for g in grps]
    return [x for x in monomodal_sections if len(x) >= min_length]


def extract_monomodal_sections(pieces, *, enforce_same_ambitus, min_length=3):
    assert isinstance(pieces, (list, tuple))
    return sum(
        [p.get_monomodal_sections(enforce_same_ambitus=enforce_same_ambitus, min_length=min_length) for p in pieces], []
    )
