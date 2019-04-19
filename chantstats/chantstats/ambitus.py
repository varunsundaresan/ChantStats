from enum import Enum
from music21.interval import Interval

__all__ = ["get_ambitus", "AmbitusType"]


class AmbitusType(str, Enum):
    """
    Possible ambitus types for pieces.
    """

    AUTHENTIC = "authentic"
    PLAGAL = "plagal"
    UNDEFINED = "undefined"


def get_ambitus(*, note_of_final, lowest_note):
    if note_of_final is None:
        return AmbitusType.UNDEFINED

    interval = Interval(note_of_final, lowest_note)
    if 0 >= interval.semitones >= -4:
        return AmbitusType.AUTHENTIC
    elif -5 >= interval.semitones > -12:
        return AmbitusType.PLAGAL
    else:
        raise Exception(  # pragma: no cover
            "Check the logic in the ambitus calculation! "
            "We expect the lowest note to be less than an octave "
            "below the main final."
        )
