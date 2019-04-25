from music21.scale import MajorScale

__all__ = ["calculate_mode_degrees"]

major_c_scale = MajorScale(tonic="C")


class ModeDegree:
    def __init__(self, *, value, alter):
        assert value in [1, 2, 3, 4, 5, 6, 7]
        assert alter in [0, -1.0]

        self.value = value
        self.alter = alter
        self.prefix = "flat-" if self.alter == -1.0 else ""
        self.descr = f"{self.prefix}{self.value}"

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


def calculate_mode_degrees(item):
    """
    Return list of mode degrees corresponding to the notes of the input item, relative to its final.

    The mode degree of the final (e.g. phrase-final, piece-final) is considered to be 1
    and the mode degrees of all other notes of the scale follow from this.

    For example, if the final is 'D3' then the sequence of notes [D3, E3, G3, G3, F3]
    has mode degrees [1, 2, 4, 4, 3].

    Parameters
    ----------
    item
        The item for which to calculate mode degrees. This can be of any type
        but it must have the attributes `notes` and `note_of_final` defined.
    """
    mode_degrees = [ModeDegree.from_note_pair(note=n, base_note=item.note_of_final) for n in item.notes]
    return mode_degrees
