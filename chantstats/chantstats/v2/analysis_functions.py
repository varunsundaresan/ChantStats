from .analysis_type import AnalysisType
from .freqs import (
    PCFreqs,
    ModeDegreeFreqs,
    L5M5Freqs,
    L5M5inMDFreqs,
    L4M4Freqs,
    L4M4inMDFreqs,
    convert_pc_based_freqs_to_mode_degree_based_freqs,
)
from .leaps_and_melodic_outlines import L5M5, L5M5inMD, L4M4, L4M4inMD
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


def calculate_leap_occurrences(item, *, unit, interval_name, cls_pcs, cls_mds):
    note_pairs_filtered = item.get_note_pairs_with_interval(interval_name)
    if unit == "pcs":
        occurrences = [cls_pcs.from_note_pair(note_pair) for note_pair in note_pairs_filtered]
    elif unit == "mode_degrees":
        occurrences = [cls_mds.from_note_pair(note_pair, base_pc=item.final) for note_pair in note_pairs_filtered]
    else:
        raise NotImplementedError()
    return occurrences


def calculate_melodic_outline_occurrences(item, *, unit, interval_name, cls_pcs, cls_mds):
    note_pairs_filtered = [mo.framing_note_pair for mo in item.get_melodic_outlines(interval_name)]
    if unit == "pcs":
        occurrences = [cls_pcs.from_note_pair(note_pair) for note_pair in note_pairs_filtered]
    elif unit == "mode_degrees":
        occurrences = [cls_mds.from_note_pair(note_pair, base_pc=item.final) for note_pair in note_pairs_filtered]
    else:
        raise NotImplementedError()
    return occurrences


def calculate_L4_occurrences(item, *, unit):
    return calculate_leap_occurrences(item, unit=unit, interval_name="P4", cls_pcs=L4M4, cls_mds=L4M4inMD)


def calculate_L5_occurrences(item, *, unit):
    return calculate_leap_occurrences(item, unit=unit, interval_name="P5", cls_pcs=L5M5, cls_mds=L5M5inMD)


def calculate_M4_occurrences(item, *, unit):
    return calculate_leap_occurrences(item, unit=unit, interval_name="M4", cls_pcs=L4M4, cls_mds=L4M4inMD)


def calculate_M5_occurrences(item, *, unit):
    return calculate_leap_occurrences(item, unit=unit, interval_name="M5", cls_pcs=L5M5, cls_mds=L5M5inMD)


def calculate_relative_L4M4_freqs(item, *, unit):
    occurrences_L4 = calculate_L4_occurrences(item, unit=unit)
    occurrences_M4 = calculate_M4_occurrences(item, unit=unit)
    all_occurrences = occurrences_L4 + occurrences_M4
    if unit == "pcs":
        freqs = L4M4Freqs(all_occurrences)
    elif unit == "mode_degrees":
        freqs = L4M4inMDFreqs(all_occurrences)
    else:
        raise NotImplementedError()

    return freqs.rel_freqs


def calculate_relative_L5M5_freqs(item, *, unit):
    occurrences_L5 = calculate_L5_occurrences(item, unit=unit)
    occurrences_M5 = calculate_M5_occurrences(item, unit=unit)
    all_occurrences = occurrences_L5 + occurrences_M5
    if unit == "pcs":
        freqs = L5M5Freqs(all_occurrences)
    elif unit == "mode_degrees":
        freqs = L5M5inMDFreqs(all_occurrences)
    else:
        raise NotImplementedError()

    return freqs.rel_freqs


def get_analysis_function(analysis):
    analysis = AnalysisType(analysis)

    if analysis == "pc_freqs":
        return calculate_relative_pc_freqs
    elif analysis == "tendency":
        return calculate_tendency
    # elif analysis == "approaches":
    #     return calculate_approaches
    elif analysis == "L_and_M__L5_u_M5":
        return calculate_relative_L5M5_freqs
    elif analysis == "L_and_M__L4_u_M4":
        return calculate_relative_L4M4_freqs
    else:
        raise NotImplementedError()
