from collections import Counter
import pandas as pd
import textwrap

__all__ = ["PCFreqs"]


class classproperty:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class BaseFreqsMeta(type):
    @property
    def zero_freqs(cls):
        # initialise the class with an empty list to obtain a "zero frequencies" object
        return cls([])


class BaseFreqs(metaclass=BaseFreqsMeta):
    """
    Base class representing absolute/relative frequencies of some entity
    (for example, of pitch classes). This base class provides all the
    machinery; derived classes only need to set ALLOWED_VALUES.
    """

    ALLOWED_VALUES = []  # derived classes need to set this to a list of allowed values

    def __init__(self, list_or_freqs):
        if isinstance(list_or_freqs, pd.Series):
            freqs = list_or_freqs
            assert list(freqs.index == self.ALLOWED_VALUES)
            self.abs_freqs = freqs
        elif isinstance(list_or_freqs, list):
            pitch_classes = list_or_freqs
            self.abs_freqs = pd.Series(Counter(pitch_classes), index=self.ALLOWED_VALUES).fillna(0, downcast="infer")
        else:
            raise ValueError(f"Cannot instantiate {self.__class__.__name__} from object: {list_or_freqs}")

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        return self.__class__(self.abs_freqs + other.abs_freqs)

    def __repr__(self):
        freqs_indented = textwrap.indent(str(self.abs_freqs), prefix="   ")
        return f"<{self.__class__.__name__}:\n\n{freqs_indented}\n>"

    @property
    def rel_freqs(self):
        return (self.abs_freqs / self.abs_freqs.sum()) * 100

    # @property
    # def zero_freqs(self):
    #     return self.__class__.zero_freqs


class PCFreqs(BaseFreqs):
    """
    Represent pitch class frequencies.
    """

    ALLOWED_VALUES = ["A", "B-", "B", "C", "D", "E", "F", "G"]


def calculate_pc_freqs_for_collection_of_phrases(phrases):
    return sum([p.pc_freqs for p in phrases], PCFreqs.zero_freqs)
