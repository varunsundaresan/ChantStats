from enum import Enum
from .freqs import PCFreqs

__all__ = ["AnalysisType", "get_analysis_function"]


class AnalysisType(str, Enum):
    PC_FREQS = "pc_freqs"
    PC_TENDENCIES = "pc_tendencies"


def calculate_relative_pc_freqs(item, unit):
    if unit == "pcs":
        # freqs = PCFreqs(analysis_input.pc)
        # freqs = analysis_input.pc_freqs.rel_freqs
        freqs = PCFreqs.from_notes(item.notes).rel_freqs
    elif unit == "mode_degrees":
        # freqs = ModeDegreeFreqs(analysis_input.mode_degrees)
        # freqs = analysis_input.mode_degree_freqs.rel_freqs
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return freqs


def get_analysis_function(analysis):
    analysis = AnalysisType(analysis)

    if analysis == "pc_freqs":
        return calculate_relative_pc_freqs
    elif analysis == "pc_tendencies":
        raise NotImplementedError()
    else:
        raise NotImplementedError()
