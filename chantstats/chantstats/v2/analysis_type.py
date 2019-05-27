from enum import Enum

__all__ = ["AnalysisType"]


class AnalysisType(str, Enum):
    PC_FREQS = ("pc_freqs", "Mode profiles", "MP", "Analysis 1 Mode Profiles: ")
    TENDENCY = ("tendency", "Tendency", "T", "Analysis 2 Tendency: ")
    # APPROACHES = ("approaches", "Leaps and Melodic Outlines", "L+M", "Analysis 3 L&M: ")

    def __new__(cls, value, desc, desc_short, plot_title_descr, **kwargs):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._description = desc
        obj._description_short = desc_short
        obj._plot_title_descr = plot_title_descr
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
    def output_path_stub(self):
        return self.value
