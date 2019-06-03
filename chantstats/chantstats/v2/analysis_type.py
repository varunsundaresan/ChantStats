from enum import Enum

__all__ = ["AnalysisType"]


class AnalysisType(str, Enum):
    PC_FREQS = ("pc_freqs", "Mode profiles", "MP", "Analysis 1 Mode Profiles: ", ("mode_profiles", ""))
    TENDENCY = ("tendency", "Tendency", "T", "Analysis 2 Tendency: ", ("tendency", ""))
    # APPROACHES = ("approaches", "Leaps and Melodic Outlines", "L+M", "Analysis 3 L&M: ")
    LEAPS_AND_MELODIC_OUTLINES_L5M5 = (
        "L_and_M__L5_u_M5",
        "Leaps and Melodic Outlines (L5 & M5)",
        "LMO",
        "Analysis 3 L&M: L5 ∪ M5: ",
        ("L_and_M", "L5_u_M5"),
    )
    LEAPS_AND_MELODIC_OUTLINES_L4M4 = (
        "L_and_M__L4_u_M4",
        "Leaps and Melodic Outlines (L4 & M4)",
        "LMO",
        "Analysis 3 L&M: L4 ∪ M4: ",
        ("L_and_M", "L4_u_M4"),
    )

    def __new__(cls, value, desc, desc_short, plot_title_descr, output_path_stubs, **kwargs):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._description = desc
        obj._description_short = desc_short
        obj._plot_title_descr = plot_title_descr
        obj._output_path_stub_1 = output_path_stubs[0]
        obj._output_path_stub_2 = output_path_stubs[1]
        return obj

    @property
    def description(self) -> str:
        return self._description

    @property
    def description_short(self) -> str:
        return self._description_short

    @property
    def plot_title_descr(self) -> str:
        return self._plot_title_descr

    @property
    def output_path_stub_1(self):
        return self._output_path_stub_1

    @property
    def output_path_stub_2(self):
        return self._output_path_stub_2
