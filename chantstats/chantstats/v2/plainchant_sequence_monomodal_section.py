from itertools import groupby
from operator import itemgetter

from .ambitus import calculate_ambitus


class MonomodalSection:
    """
    Represents a section of consecutive phrases in a given piece with the same phrase-final.
    """

    def __init__(self, piece, idx_start, idx_end):
        # assert piece.__class__.__name__ == "PlainchantSequencePiece"
        assert "PlainchantSequencePiece" in [cls.__name__ for cls in piece.__class__.__mro__]
        self.piece = piece
        self.idx_start = idx_start
        self.idx_end = idx_end
        self.phrases = piece.phrases[idx_start - 1 : idx_end]
        self.notes = sum([p.notes for p in self.phrases], [])
        # self.length = len(self.phrases)
        self.num_phrases = len(self.phrases)
        self.num_notes = len(self.notes)
        if len(set(p.phrase_final for p in self.phrases)) != 1:
            error_msg = (
                f"Non-unique phrase final: {set(p.phrase_final for p in self.phrases)}"
                f"(section: {self.idx_start}-{self.idx_end})"
            )
            raise ValueError(error_msg)
        self.note_of_final = self.phrases[0].notes[-1]
        assert self.note_of_final == self.phrases[-1].notes[-1]  # sanity check
        self.lowest_note = min([p.lowest_note for p in self.phrases])
        self.final = self.phrases[0].phrase_final
        assert self.final == self.phrases[-1].phrase_final  # sanity check
        self.ambitus = calculate_ambitus(self)
        self.descr = f"s{self.piece.number:02d}.{self.final}.mm_{self.idx_start:02d}_{self.idx_end:02d}"

        self.pitch_classes = sum([p.pitch_classes for p in self.phrases], [])
        self.pc_pairs = sum([p.pc_pairs for p in self.phrases], [])
        self.note_pairs = sum([p.note_pairs for p in self.phrases], [])
        self.mode_degrees = sum([p.mode_degrees for p in self.phrases], [])
        self.mode_degree_pairs = sum([p.mode_degree_pairs for p in self.phrases], [])

    def __repr__(self):
        s = (
            f"<MonomodalSection: '{self.piece.filename_short}', "
            f"phrase-final '{self.final}', "
            f"phrases {self.idx_start}-{self.idx_end} "
            f"({self.num_phrases} phrases, {self.num_notes} notes), "
            f"ambitus={self.ambitus.value!r}>"
        )
        return s

    def __lt__(self, other):
        return (self.piece.number, self.idx_start) < (other.piece.number, other.idx_start)

    def get_melodic_outlines(self, interval, *, allow_thirds=False):
        return sum([p.get_melodic_outlines(interval, allow_thirds=allow_thirds) for p in self.phrases], [])

    def get_note_pairs_with_interval(self, interval_name):
        return sum([p.get_note_pairs_with_interval(interval_name) for p in self.phrases], [])


def extract_monomodal_sections_from_piece(piece, *, enforce_same_phrase_ambitus, min_num_phrases=3, min_num_notes=80):
    """
    Extract monomodal sections (= sections of consecutive phrases with the same phrase-final).

    Parameters
    ----------
    piece : PlainchantSequencePiece
        The piece from which to extract monomodal sections.
    enforce_same_phrase_ambitus: boolean
        If True, all phrases in the monomodal section must have
        the same ambitus (in addition to the same phrase-final).
    min_num_phrases : int
        Minimum number of phrases for a section to be included in the
        result (any phrase sections with fewer phrases are discarded).
    min_num_notes : int
        Minimum number of notes for a section to be included in the
        result (any phrase sections with fewer notes are discarded).

    Returns
    -------
    list of MonomodalSection
    """
    if enforce_same_phrase_ambitus:
        key_func = lambda phrase: (phrase.note_of_final, phrase.ambitus)
    else:
        key_func = lambda phrase: phrase.note_of_final

    get_idx_start = lambda grp: grp[1][0][0]
    get_idx_end = lambda grp: grp[1][-1][0]

    items = [key_func(p) for p in piece.phrases]
    grps = [(x, list(grp)) for x, grp in groupby(enumerate(items, start=1), key=itemgetter(1))]
    monomodal_sections = [MonomodalSection(piece, get_idx_start(g), get_idx_end(g)) for g in grps]
    monomodal_sections_filtered = [
        x for x in monomodal_sections if x.num_phrases >= min_num_phrases and x.num_notes >= min_num_notes
    ]
    return monomodal_sections_filtered


def extract_monomodal_sections(pieces, *, enforce_same_phrase_ambitus, min_num_phrases=3, min_num_notes=80):
    assert isinstance(pieces, (list, tuple))
    return sum(
        [
            p.get_monomodal_sections(
                enforce_same_phrase_ambitus=enforce_same_phrase_ambitus,
                min_num_phrases=min_num_phrases,
                min_num_notes=min_num_notes,
            )
            for p in pieces
        ],
        [],
    )
