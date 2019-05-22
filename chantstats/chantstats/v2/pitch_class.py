from enum import Enum

__all__ = ["PC"]


class PC(str, Enum):
    """
    Represents occurring pitch classes.
    """

    A = "A"
    B_FLAT = "B-"
    B = "B"
    C = "C"
    D = "D"
    E_FLAT = "E-"
    E = "E"
    F = "F"
    G = "G"

    @property
    def descr(self):
        return self.value

    @classmethod
    def from_note(cls, note):
        return cls(note.name)

    @property
    def allowed_values(self):
        return list(PC)
