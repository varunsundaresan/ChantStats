from enum import Enum
from music21.interval import Interval

__all__ = ["AmbitusType", "calculate_ambitus"]


class AmbitusType(str, Enum):
    """
    Possible ambitus types for pieces.
    """

    AUTHENTIC = "authentic"
    PLAGAL = "plagal"
    UNDEFINED = "undefined"


def calculate_ambitus(item):
    """
    Calculate the ambitus of a phrase, monomodal section, piece, etc.

    Parameters
    ----------
    item
        The item for which to calculate the ambitus. This can be of
        any type, but it must have the attributes `lowest_note` and
        `note_of_final` defined.
    """
    if item.note_of_final is None:
        return AmbitusType.UNDEFINED

    interval = Interval(item.note_of_final, item.lowest_note)
    if 0 >= interval.semitones >= -4:
        return AmbitusType.AUTHENTIC
    elif -5 >= interval.semitones > -12:
        return AmbitusType.PLAGAL
    elif interval.semitones == -12:
        # TODO: which ambitus should this have?
        return AmbitusType.PLAGAL
    else:
        raise Exception(  # pragma: no cover
            "Check the logic in the ambitus calculation! "
            "We expect the lowest note to be less than an octave "
            "below the main final."
        )
