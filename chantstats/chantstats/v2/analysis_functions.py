from enum import Enum
from .freqs import PCFreqs, ModeDegreeFreqs
from .tendencies import PCTendencies, ModeDegreeTendencies, PCApproaches

__all__ = ["AnalysisType", "get_analysis_function"]


class AnalysisType(str, Enum):
    PC_FREQS = "pc_freqs"
    PC_TENDENCIES = "pc_tendencies"
    APPROACHES = "approaches"

    @property
    def output_path_stub(self):
        return self.value


def calculate_relative_pc_freqs(item, unit):
    if unit == "pcs":
        freqs = PCFreqs.from_notes(item.notes)
    elif unit == "mode_degrees":
        freqs = ModeDegreeFreqs.from_notes_and_final(item.notes, item.note_of_final)
    else:
        raise NotImplementedError()

    return freqs.rel_freqs


def calculate_pc_tendencies(item, unit, *, using="condprobs_v1"):
    if unit == "pcs":
        tendencies = PCTendencies(item)
    elif unit == "mode_degrees":
        tendencies = ModeDegreeTendencies(item)
    else:
        raise NotImplementedError()

    return tendencies.as_series(using=using)


def calculate_approaches(item, unit, *, using="condprobs_v1"):
    if unit == "pcs":
        tendencies = PCApproaches(item)
    elif unit == "mode_degrees":
        # tendencies = ModeDegreeApproaches(item)
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tendencies.as_series(using=using)


def get_analysis_function(analysis):
    analysis = AnalysisType(analysis)

    if analysis == "pc_freqs":
        return calculate_relative_pc_freqs
    elif analysis == "pc_tendencies":
        return calculate_pc_tendencies
    elif analysis == "approaches":
        return calculate_approaches
    else:
        raise NotImplementedError()
