from enum import Enum

__all__ = ["PC"]


class PC(str, Enum):
    """
    Represents occurring pitch classes.
    """

    D = ("D", "D")
    E_FLAT = ("E-", "E♭")
    E = ("E", "E")
    F = ("F", "F")
    F_SHARP = ("F#", "F♯")
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

    @property
    def label_for_plots(self):
        return self._str_value

    @property
    def _number_prefix(self):
        # index of this PC in the list of occurring pitch classes
        return self.allowed_values.index(self) + 1

    @property
    def value_with_number_prefix(self):
        return f"{self._number_prefix:02d}.{self.value}"

    @classmethod
    def from_note(cls, note):
        return cls(note.name)

    @classmethod
    def get_class_description(cls):
        return "Pitch class"

    # Note: the method 'in_mode_degrees()' is dynamically added to this class in
    # the module `mode_degree.py` (this is necessary to avoid a circular import).
    #
    # def in_mode_degrees(self):
    #     raise NotImplementedError("This is implemented in mode_degree.py")


PC.allowed_values = list(PC)
