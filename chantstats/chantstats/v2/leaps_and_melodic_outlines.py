from .note_pair import NotePair
from .mode_degree import ModeDegree
from .pitch_class import PC

__all__ = ["L5M5"]


class L5M5:
    def __init__(self, *, bottom_pc, top_pc):
        # assert isinstance(bottom_pc, PC)
        # assert isinstance(top_pc, PC)
        self.bottom_pc = PC(bottom_pc)
        self.top_pc = PC(top_pc)

    def __repr__(self):
        return f"pcs{self.bottom_pc}^{self.top_pc}_L5M5"

    def __eq__(self, other):
        return self.bottom_pc == other.bottom_pc and self.top_pc == other.top_pc

    def __lt__(self, other):
        # Note: this ordering relation doesn't really have much meaning, but we
        # need to implement __lt__ in order to be able to sort lists containing
        # L5M5 objects.
        return self.bottom_pc < other.bottom_pc

    def __hash__(self):
        return hash((self.bottom_pc, self.top_pc))

    @property
    def str_value(self):
        return rf"pcs$\stackrel{{{self.top_pc}}}{{{self.bottom_pc}}}$_L5M5"
        # return f"pcs${{\mathrm{{{self.top_pc}}}}}^{{\mathrm{{{self.bottom_pc}}}}}$_L5M5"

    @property
    def label_for_plots(self):
        return rf"pcs$\stackrel{{{self.top_pc.label_for_plots}}}{{{self.bottom_pc.label_for_plots}}}$_L5M5"

    @classmethod
    def from_note_pair(cls, note_pair):
        assert isinstance(note_pair, NotePair)
        if not note_pair.semitones == 7:
            raise ValueError(f"Not an instance of L5 or M5: {note_pair}")
        return cls(bottom_pc=note_pair.bottom_pc, top_pc=note_pair.top_pc)

    def in_mode_degrees(self, *, base_pc):
        bottom_md = ModeDegree.from_pc_pair(pc=self.bottom_pc, base_pc=base_pc)
        top_md = ModeDegree.from_pc_pair(pc=self.top_pc, base_pc=base_pc)
        return L5M5inMD(bottom_md=bottom_md, top_md=top_md)


L5M5.allowed_values = [
    L5M5(bottom_pc=PC("D"), top_pc=PC("A")),
    L5M5(bottom_pc=PC("E"), top_pc=PC("B")),
    L5M5(bottom_pc=PC("F"), top_pc=PC("C")),
    L5M5(bottom_pc=PC("G"), top_pc=PC("D")),
    L5M5(bottom_pc=PC("A"), top_pc=PC("E")),
    L5M5(bottom_pc=PC("B-"), top_pc=PC("F")),
    L5M5(bottom_pc=PC("C"), top_pc=PC("G")),
]


class L5M5inMD:
    def __init__(self, *, bottom_md, top_md):
        assert isinstance(bottom_md, ModeDegree)
        assert isinstance(top_md, ModeDegree)
        self.bottom_md = bottom_md
        self.top_md = top_md

    def __repr__(self):
        return f"mds{self.bottom_md}^{self.top_md}_L5"

    def __eq__(self, other):
        return self.bottom_md == other.bottom_md and self.top_md == other.top_md

    def __lt__(self, other):
        # Note: this ordering relation doesn't really have much meaning, but we
        # need to implement __lt__ in order to be able to sort lists containing
        # L5M5 objects.
        return self.bottom_md < other.bottom_md

    def __hash__(self):
        return hash((self.bottom_md, self.top_md))

    @property
    def str_value(self):
        return rf"mds$\stackrel{{{self.top_md.descr}}}{{{self.bottom_md.descr}}}$_L5"
        # return f"pcs${{\mathrm{{{self.top_md.descr}}}}}^{{\mathrm{{{self.bottom_md.descr}}}}}$_L5"

    @property
    def label_for_plots(self):
        return rf"mds$\stackrel{{{self.top_md.label_for_plots}}}{{{self.bottom_md.label_for_plots}}}$_L5"

    @classmethod
    def from_note_pair(cls, note_pair, *, base_pc):
        assert isinstance(note_pair, NotePair)
        if not note_pair.semitones == 7:
            raise ValueError(f"Not a leap L5: {note_pair}")
        bottom_md = ModeDegree.from_pc_pair(pc=note_pair.bottom_pc, base_pc=base_pc)
        top_md = ModeDegree.from_pc_pair(pc=note_pair.top_pc, base_pc=base_pc)
        return cls(bottom_md=bottom_md, top_md=top_md)


L5M5inMD.allowed_values = [
    L5M5inMD(bottom_md=ModeDegree(value=1), top_md=ModeDegree(value=5)),
    L5M5inMD(bottom_md=ModeDegree(value=2), top_md=ModeDegree(value=6)),
    L5M5inMD(bottom_md=ModeDegree(value=3), top_md=ModeDegree(value=7)),
    L5M5inMD(bottom_md=ModeDegree(value=4), top_md=ModeDegree(value=1)),
    L5M5inMD(bottom_md=ModeDegree(value=5), top_md=ModeDegree(value=2)),
    L5M5inMD(bottom_md=ModeDegree(value=6), top_md=ModeDegree(value=3)),
    L5M5inMD(bottom_md=ModeDegree(value=7), top_md=ModeDegree(value=4)),
]
