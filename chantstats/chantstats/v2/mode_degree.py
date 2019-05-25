__all__ = ["ModeDegree"]


class ModeDegree:
    def __init__(self, *, value, alter=0):
        assert value in [1, 2, 3, 4, 5, 6, 7]
        assert alter in [0, -1.0]

        self.value = value
        self.alter = alter
        self.prefix = "flat-" if self.alter == -1.0 else ""
        self.descr = f"{self.prefix}{self.value}"
        self.str_prefix = "♭" if self.alter == -1.0 else ""
        # self.str_value = f"{self.str_prefix}{self.value}\u0302"  # same as 'descr', but with a hat symbol over the number
        self.str_value = (
            f"{self.str_prefix}$\widehat{self.value}$"
        )  # same as 'descr', but with a hat symbol over the number

    @classmethod
    def from_note_pair(self, *, note, base_note):
        diatonic_distance = (note.pitch.diatonicNoteNum - base_note.pitch.diatonicNoteNum) % 7 + 1
        alter = note.pitch.alter

        if alter not in [0, -1.0]:  # pragma: no cover
            raise NotImplementedError(f"Unexpected alteration of note: '{note.nameWithOctave}'")

        return ModeDegree(value=diatonic_distance, alter=alter)

    def __repr__(self):
        return f"<ModeDegree: {self.descr}>"

    def __str__(self):
        return self.descr

    def __format__(self, fmt):
        return f"{self.prefix}{self.value}\u0302"

    def __eq__(self, other):
        if isinstance(other, int):
            return self.alter == 0 and self.value == other
        elif isinstance(other, str):
            return self.descr == other
        elif isinstance(other, ModeDegree):
            return self.value == other.value and self.alter == other.alter
        else:
            raise TypeError(f"Cannot compare ModeDegree to object of type {type(other)}")

    def __lt__(self, other):
        return (self.value < other.value) or (self.value == other.value and self.alter < other.alter)

    def __hash__(self):
        return hash((self.value, self.alter))


ModeDegree.allowed_values = [
    ModeDegree(value=1, alter=-1),
    ModeDegree(value=1, alter=0),
    ModeDegree(value=2, alter=-1),
    ModeDegree(value=2, alter=0),
    ModeDegree(value=3, alter=-1),
    ModeDegree(value=3, alter=0),
    ModeDegree(value=4, alter=0),
    ModeDegree(value=5, alter=0),
    ModeDegree(value=6, alter=-1),
    ModeDegree(value=6, alter=0),
    ModeDegree(value=7, alter=-1),
    ModeDegree(value=7, alter=0),
]
