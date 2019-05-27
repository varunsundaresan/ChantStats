__all__ = ["ModeDegree"]

import pandas as pd
from .pitch_class import PC

__all__ = ["ModeDegree"]


class ModeDegree:
    def __init__(self, *, value, alter=0):
        assert value in [1, 2, 3, 4, 5, 6, 7]
        assert alter in [0, -1.0, +1.0]

        self.value = value
        self.alter = alter
        self.prefix = "flat-" if self.alter == -1.0 else ("#" if self.alter == +1.0 else "")
        self.descr = f"{self.prefix}{self.value}"
        self.str_prefix = "♭" if self.alter == -1.0 else ("♯" if self.alter == +1.0 else "")
        # self.str_value = f"{self.str_prefix}{self.value}\u0302"  # same as 'descr', but with a hat symbol over the number
        self.str_value = (
            f"{self.str_prefix}$\widehat{self.value}$"
        )  # same as 'descr', but with a hat symbol over the number
        self.label_for_plots = f"{self.str_prefix}{self.value}"  # same as 'str_value', but without the hat symbol

    @classmethod
    def from_note_pair(self, *, note, base_note):
        diatonic_distance = (note.pitch.diatonicNoteNum - base_note.pitch.diatonicNoteNum) % 7 + 1
        alter = note.pitch.alter

        # special case
        if base_note.name == "B-":
            if note.name == "B-":
                alter = 0
            elif note.name == "B":
                raise NotImplementedError()
            else:
                # all other cases are covered
                pass

        if alter not in [0, -1.0]:  # pragma: no cover
            raise NotImplementedError(
                f"Unexpected alteration of note '{note.nameWithOctave}' compared to base note '{base_note.nameWithOctave}'"
            )

        return ModeDegree(value=diatonic_distance, alter=alter)

    @classmethod
    def from_other(cls, value):
        if isinstance(value, ModeDegree):
            return value
        elif isinstance(value, int):
            return ModeDegree(value=value)
        else:
            raise NotImplementedError()

    @classmethod
    def from_pc_pair(self, *, pc, base_pc):
        return df_mode_degrees[base_pc][pc]

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

    @classmethod
    def get_class_description(cls):
        return "Mode degree"


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


def convert_to_mode_degree(x):
    if isinstance(x, int):
        return ModeDegree(value=x)
    elif isinstance(x, str):
        if x.startswith("flat-"):
            value = int(x[-1])
            return ModeDegree(value=value, alter=-1)
        elif x.startswith("#"):
            value = int(x[-1])
            return ModeDegree(value=value, alter=+1)
        else:
            raise ValueError(f"Invalid mode degree: {x}")
    else:
        raise TypeError(f"Invalid mode degree: {x}")


df_mode_degrees = pd.DataFrame(
    [
        [1, 7, 6, 5, 4, 3, 3, 2],
        [2, 1, 7, 6, 5, 4, 4, 3],
        [3, 2, 1, 7, 6, 5, 5, 4],
        [4, 3, 2, 1, 7, 6, 6, 5],
        [5, 4, 3, 2, 1, 7, 7, 6],
        ["flat-6", "flat-5", "flat-4", "flat-3", "flat-2", 1, "flat-1", "flat-7"],
        [6, 5, 4, 3, 2, "#1", 1, 7],
        [7, 6, 5, 4, 3, 2, 2, 1],
    ],
    columns=PC.allowed_values,
    index=PC.allowed_values,
)


df_mode_degrees = df_mode_degrees.applymap(convert_to_mode_degree)


def convert_pc_to_mode_degree(self, *, base_pc):
    return ModeDegree.from_pc_pair(pc=self, base_pc=base_pc)


# Note: we add the method `in_mode_degrees()` dynamically to the class `PC` here
# in order to avoid a circular import.
PC.in_mode_degrees = convert_pc_to_mode_degree
