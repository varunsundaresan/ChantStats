from collections import Counter
import pandas as pd

__all__ = ["PCFreqs"]

ALLOWED_PITCH_CLASSES = ["A", "B-", "B", "C", "D", "E", "F", "G"]


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

    abs_freqs = None

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        return self.__class__(self.abs_freqs + other.abs_freqs)

    @property
    def rel_freqs(self):
        return (self.abs_freqs / self.abs_freqs.sum()) * 100

    # @property
    # def zero_freqs(self):
    #     return self.__class__.zero_freqs


class PCFreqs(BaseFreqs):
    def __init__(self, pitch_classes_or_freqs):
        if isinstance(pitch_classes_or_freqs, pd.Series):
            freqs = pitch_classes_or_freqs
            assert list(freqs.index == ALLOWED_PITCH_CLASSES)
            self.abs_freqs = freqs
        elif isinstance(pitch_classes_or_freqs, list):
            pitch_classes = pitch_classes_or_freqs
            self.abs_freqs = pd.Series(Counter(pitch_classes), index=ALLOWED_PITCH_CLASSES).fillna(0, downcast="infer")
        else:
            raise ValueError(f"Cannot instantiate PCFreqs from object: {pitch_classes_or_freqs}")


def calculate_pc_freqs_for_collection_of_phrases(phrases):
    return sum([p.pc_freqs for p in phrases], PCFreqs.zero_freqs)
