import os
from abc import ABCMeta

from chantstats.unit import UnitType
from chantstats.utils import EnumWithDescription
from .modal_category import ModalCategory

__all__ = ["FullAnalysisSpec"]


class RepertoireAndGenreType(EnumWithDescription):
    PLAINCHANT_SEQUENCES = ("plainchant_sequences", "Plainchant Sequences", ("chant", "sequences"))
    RESPONSORIAL_CHANTS = ("responsorial_chants", "Responsorial Chants", ("chant", "responsorial_chants"))
    ORGANA = ("organa", "Organa", ("organum", ""))

    def __new__(cls, name, desc, output_path_stubs, **kwargs):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj._description = desc
        obj.output_path_stub_1 = output_path_stubs[0]
        obj.output_path_stub_2 = output_path_stubs[1]
        return obj


class BaseAnalysisFunc(metaclass=ABCMeta):
    def __call__(self, item):
        raise NotImplementedError()


class AnalysisFuncPCFreqs(BaseAnalysisFunc):
    def __init__(self, abs_or_rel):
        assert abs_or_rel in ["abs_freqs", "rel_freqs"]
        self.abs_or_rel = abs_or_rel

    def __call__(self, item, *, unit):
        if unit == UnitType.PCS:
            return getattr(item.pc_freqs, self.abs_or_rel)
        elif unit == UnitType.MODE_DEGREES:
            return getattr(item.mode_degree_freqs, self.abs_or_rel)
        else:
            raise RuntimeError("Unexpected unit: {self.unit}")


class AnalysisType(EnumWithDescription):
    PC_FREQS = ("pc_freqs", "PC Frequencies")
    TENDENCY = ("pc_tendencies", "PC Tendencies")
    APPROACHES_AND_DEPARTURES = ("approaches_and_departures", "Approaches & Departures")
    LEAPS_AND_MELODIC_OUTLINES = ("leaps_and_melodic_outlines", "Leaps & Melodic Outlines")

    @property
    def output_path_stub(self):
        return self.value

    @property
    def analysis_func(self):
        if self.value == "pc_freqs":
            return AnalysisFuncPCFreqs("rel_freqs")
        else:
            return BaseAnalysisFunc()


class ModeType(EnumWithDescription):
    BY_FINAL = ("by_final", "by final")
    AUTHENTIC_MODES = ("authentic_modes", "authentic modes")
    PLAGAL_MODES = ("plagal_modes", "plagal modes")

    def get_description(self, *, final):
        # TODO: check that final is a valid pitch class
        if self.value == "by_final":
            return f"{final}-final"
        elif self.value == "authentic_modes":
            return f"{final}-authentic"
        elif self.value == "plagal_modes":
            return f"{final}-plagal"
        else:
            raise RuntimeError(f"Unexpected value: {self.value!r}")

    def get_subfolder(self, *, final):
        # TODO: check that final is a valid pitch class
        if self.value == "by_final":
            return f"{final}_final"
        elif self.value == "authentic_modes":
            return f"{final}_authentic"
        elif self.value == "plagal_modes":
            return f"{final}_plagal"
        else:
            raise RuntimeError(f"Unexpected value: {self.value!r}")
