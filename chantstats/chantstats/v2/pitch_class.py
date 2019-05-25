from enum import Enum

__all__ = ["PC"]


class PC(str, Enum):
    """
    Represents occurring pitch classes.
    """

    D = ("D", "D")
    # E_FLAT = ("E-", "E♭")
    E = ("E", "E")
    F = ("F", "F")
    G = ("G", "G")
    A = ("A", "A")
    B_FLAT = ("B-", "B♭")
    B = ("B", "B")
    C = ("C", "C")

    def __new__(cls, name, str_value, **kwargs):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj._str_value = str_value
        return obj

    @property
    def descr(self):
        return self.value

    @property
    def str_value(self):
        return self._str_value

    @classmethod
    def from_note(cls, note):
        return cls(note.name)


PC.allowed_values = list(PC)
