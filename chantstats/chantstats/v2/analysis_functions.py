from .analysis_type import AnalysisType
from .freqs import PCFreqs, ModeDegreeFreqs
from .tendency import PCTendency, ModeDegreeTendency

__all__ = ["get_analysis_function"]


def calculate_relative_pc_freqs(item, unit):
    if unit == "pcs":
        freqs = PCFreqs.from_notes(item.notes)
    elif unit == "mode_degrees":
        freqs = ModeDegreeFreqs.from_notes_and_final(item.notes, item.note_of_final)
    else:
        raise NotImplementedError()

    return freqs.rel_freqs


def calculate_tendency(item, unit, *, using="condprobs_v1"):
    if unit == "pcs":
        tendency = PCTendency(item)
    elif unit == "mode_degrees":
        tendency = ModeDegreeTendency(item)
    else:
        raise NotImplementedError()

    return tendency.as_series(using=using)


# def calculate_approaches(item, unit, *, using="condprobs_v1"):
#     if unit == "pcs":
#         tendency = PCApproaches(item)
#     elif unit == "mode_degrees":
#         # tendency = ModeDegreeApproaches(item)
#         raise NotImplementedError()
#     else:
#         raise NotImplementedError()
#
#     return tendency.as_series(using=using)


def get_analysis_function(analysis):
    analysis = AnalysisType(analysis)

    if analysis == "pc_freqs":
        return calculate_relative_pc_freqs
    elif analysis == "tendency":
        return calculate_tendency
    # elif analysis == "approaches":
    #     return calculate_approaches
    else:
        raise NotImplementedError()
