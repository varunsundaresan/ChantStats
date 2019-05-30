from music21.interval import Interval, Direction
from music21.note import Note
from .interval_type import IntervalType
from .logging import logger


class LargeIntervalError(Exception):
    """
    Indicates unexpectedly large intervals between consecutive notes.
    """


class NotePair:
    def __init__(self, note1, note2):
        assert isinstance(note1, Note)
        assert isinstance(note2, Note)
        self.note1 = note1
        self.note2 = note2
        self.interval = Interval(self.note1, self.note2)
        self.pc1 = self.note1.name
        self.pc2 = self.note2.name
        self.semitones = abs(self.interval.semitones)
        self.direction = self.interval.direction
        if self.direction == Direction.ASCENDING:
            self.bottom_pc = self.pc1
            self.top_pc = self.pc2
        else:
            self.bottom_pc = self.pc2
            self.top_pc = self.pc1

    def is_interval(self, interval_name):
        assert isinstance(interval_name, str)
        return self.interval.name == interval_name

    def __repr__(self):
        return f"<NotePair: ({self.note1}, {self.note2})>"

    def __iter__(self):
        yield self.note1
        yield self.note2

    def _classify_interval(self, version):
        if version == "v1":
            min_semitones_leap = 3
        elif version == "v2":
            min_semitones_leap = 4
        else:
            raise ValueError(f"Invalid interval type version: '{version}'")

        if self.semitones == 0:
            return IntervalType.COMMON_TONE
        elif self.semitones < min_semitones_leap:
            return IntervalType.STEP
        elif self.semitones <= 11:
            return IntervalType.LEAP
        elif self.semitones == 12:
            logger.warning(f"Interval is an octave: note1={self.note1}, note2={self.note2}.")
            # raise LargeIntervalError(f"Interval is an octave: note1={self.note1}, note2={self.note2}.")
            return IntervalType.LEAP
        else:
            raise LargeIntervalError(
                f"Interval larger than an octave: note1={self.note1}, note2={self.note2}. Please investigate!"
            )

    @property
    def interval_type_v1(self):
        return self._classify_interval(version="v1")

    @property
    def interval_type_v2(self):
        return self._classify_interval(version="v2")
