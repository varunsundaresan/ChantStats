from .note_pair import NotePair
from .mode_degree import ModeDegree
from .pitch_class import PC

__all__ = ["LeapL5"]


class LeapL5:
    def __init__(self, *, bottom_pc, top_pc):
        # assert isinstance(bottom_pc, PC)
        # assert isinstance(top_pc, PC)
        self.bottom_pc = PC(bottom_pc)
        self.top_pc = PC(top_pc)

    def __repr__(self):
        return f"pcs{self.bottom_pc}^{self.top_pc}_L5"

    def __eq__(self, other):
        return self.bottom_pc == other.bottom_pc and self.top_pc == other.top_pc

    def __lt__(self, other):
        # Note: this ordering relation doesn't really have much meaning, but we
        # need to implement __lt__ in order to be able to sort lists containing
        # LeapL5 objects.
        return self.bottom_pc < other.bottom_pc

    def __hash__(self):
        return hash((self.bottom_pc, self.top_pc))

    #     @property
    #     def str_value(self):
    #         return rf"pcs$\stackrel{{{self.top_pc}}}{{{self.bottom_pc}}}$_L5"
    #         #return f"pcs${{\mathrm{{{self.top_pc}}}}}^{{\mathrm{{{self.bottom_pc}}}}}$_L5"

    @classmethod
    def from_note_pair(cls, note_pair):
        assert isinstance(note_pair, NotePair)
        if not note_pair.semitones == 7:
            raise ValueError(f"Not a leap L5: {note_pair}")
        return cls(bottom_pc=note_pair.bottom_pc, top_pc=note_pair.top_pc)

    def in_mode_degrees(self, *, base_pc):
        bottom_md = ModeDegree.from_pc_pair(pc=self.bottom_pc, base_pc=base_pc)
        top_md = ModeDegree.from_pc_pair(pc=self.top_pc, base_pc=base_pc)
        return LeapL5inMD(bottom_md=bottom_md, top_md=top_md)


LeapL5.allowed_values = [
    LeapL5(bottom_pc=PC("D"), top_pc=PC("A")),
    LeapL5(bottom_pc=PC("E"), top_pc=PC("B")),
    LeapL5(bottom_pc=PC("F"), top_pc=PC("C")),
    LeapL5(bottom_pc=PC("G"), top_pc=PC("D")),
    LeapL5(bottom_pc=PC("A"), top_pc=PC("E")),
    LeapL5(bottom_pc=PC("B-"), top_pc=PC("F")),
    LeapL5(bottom_pc=PC("C"), top_pc=PC("G")),
]


class LeapL5inMD:
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
        # LeapL5 objects.
        return self.bottom_md < other.bottom_md

    def __hash__(self):
        return hash((self.bottom_md, self.top_md))

    #     @property
    #     def str_value(self):
    #         return rf"pcs$\stackrel{{{self.top_pc}}}{{{self.bottom_pc}}}$_L5"
    #         #return f"pcs${{\mathrm{{{self.top_pc}}}}}^{{\mathrm{{{self.bottom_pc}}}}}$_L5"
    #
    # @classmethod
    # def from_note_pair(cls, note_pair):
    #     assert isinstance(note_pair, NotePair)
    #     if not note_pair.semitones == 7:
    #         raise ValueError(f"Not a leap L5: {note_pair}")
    #     return cls(bottom_pc=note_pair.bottom_pc, top_pc=note_pair.top_pc)


LeapL5inMD.allowed_values = [
    LeapL5inMD(bottom_md=ModeDegree(value=1), top_md=ModeDegree(value=5)),
    LeapL5inMD(bottom_md=ModeDegree(value=2), top_md=ModeDegree(value=6)),
    LeapL5inMD(bottom_md=ModeDegree(value=3), top_md=ModeDegree(value=7)),
    LeapL5inMD(bottom_md=ModeDegree(value=4), top_md=ModeDegree(value=1)),
    LeapL5inMD(bottom_md=ModeDegree(value=5), top_md=ModeDegree(value=2)),
    LeapL5inMD(bottom_md=ModeDegree(value=6), top_md=ModeDegree(value=3)),
    LeapL5inMD(bottom_md=ModeDegree(value=7), top_md=ModeDegree(value=4)),
]
