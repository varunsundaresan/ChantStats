from .note_pair import NotePair

__all__ = ["LeapL5"]


class LeapL5:
    def __init__(self, *, bottom_pc, top_pc):
        self.bottom_pc = bottom_pc
        self.top_pc = top_pc

    def __repr__(self):
        return f"pcs{self.bottom_pc}^{self.top_pc}_L5"

    def __eq__(self, other):
        return self.bottom_pc == other.bottom_pc and self.top_pc == other.top_pc

    def __lt__(self, other):
        # Note: this ordering relation doesn't really have much meaning, but we
        # need to implement __lt__ in order to be able to sort lists containing
        # LeapL5 object.s
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


LeapL5.allowed_values = [
    LeapL5(bottom_pc="D", top_pc="A"),
    LeapL5(bottom_pc="E", top_pc="B"),
    LeapL5(bottom_pc="F", top_pc="C"),
    LeapL5(bottom_pc="G", top_pc="D"),
    LeapL5(bottom_pc="A", top_pc="E"),
    LeapL5(bottom_pc="B-", top_pc="F"),
    LeapL5(bottom_pc="C", top_pc="G"),
]
