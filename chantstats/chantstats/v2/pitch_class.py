from enum import Enum

__all__ = ["PC"]


class PC(str, Enum):
    """
    Represents occurring pitch classes.
    """

    A = "A"
    B = "B"
    B_FLAT = "B-"
    C = "C"
    D = "D"
    E_FLAT = "E-"
    E = "E"
    F = "F"
    G = "G"

    @classmethod
    def from_note(cls, note):
        return cls(note.name)
