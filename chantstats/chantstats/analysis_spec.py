import os
from abc import ABCMeta
from enum import Enum

from .dendrogram2 import Dendrogram
from .modal_category import ModalCategory

__all__ = ["FullAnalysisSpec"]


class EnumWithDescription(str, Enum):
    def __new__(cls, name, desc, **kwargs):
        obj = str.__new__(cls)
        obj._value_ = name
        obj._description = desc
        return obj

    @property
    def description(self) -> str:
        """
        Returns
        -------
        str
            Long form description of this state suitable for use in plot titles etc.
        """
        return self._description


class RepertoireAndGenreType(EnumWithDescription):
    PLAINCHANT_SEQUENCES = ("plainchant_sequences", "Plainchant Sequences", ("chant", "sequences"))
    RESPONSORIAL_CHANTS = ("responsorial_chants", "Responsorial Chants", ("chant", "responsorial_chants"))
    ORGANA = ("organa", "Organa", ("organum", ""))

    def __new__(cls, name, desc, path_stubs, **kwargs):
        obj = str.__new__(cls)
        obj._value_ = name
        obj._description = desc
        obj.path_stub_1 = path_stubs[0]
        obj.path_stub_2 = path_stubs[1]
        return obj


class BaseAnalysisFunc(metaclass=ABCMeta):
    def __call__(self, item):
        raise NotImplementedError()


class AnalysisFuncPCFreqs(BaseAnalysisFunc):
    def __init__(self, abs_or_rel):
        assert abs_or_rel in ["abs_freqs", "rel_freqs"]
        self.abs_or_rel = abs_or_rel

    def __call__(self, item):
        return getattr(item.pc_freqs, self.abs_or_rel)


class AnalysisType(EnumWithDescription):
    PC_FREQS = ("pc_freqs", "PC Frequencies")
    TENDENCY = ("tendency", "Tendency")
    APPROACHES_AND_DEPARTURES = ("approaches_and_departures", "Approaches & Departures")
    LEAPS_AND_MELODIC_OUTLINES = ("leaps_and_melodic_outlines", "Leaps & Melodic Outlines")

    @property
    def analysis_func(self):
        if self.value == "pc_freqs":
            return AnalysisFuncPCFreqs("rel_freqs")
        else:
            return BaseAnalysisFunc()


class UnitType(EnumWithDescription):
    PCS = ("pcs", "pitch classes")
    MODE_DEGREES = ("mode_degrees", "mode degrees")


class ModeType(EnumWithDescription):
    BY_FINAL = ("by_final", "by final")
    AUTHENTIC_MODES = ("authentic_modes", "authentic modes")
    PLAGAL_MODES = ("plagal_modes", "plagal modes")

    def get_description(self, final):
        # TODO: check that final is a valid pitch class
        if self.value == "by_final":
            return f"{final}-final"
        elif self.value == "authentic_modes":
            return f"{final}-authentic"
        elif self.value == "plagal_modes":
            return f"{final}-plagal"
        else:
            raise RuntimeError(f"Unexpected value: {self.value!r}")


class FullAnalysisSpec:
    def __init__(self, *, repertoire_and_genre, analysis, unit, mode):
        self.repertoire_and_genre = RepertoireAndGenreType(repertoire_and_genre)
        self.analysis = AnalysisType(analysis)
        self.unit = UnitType(unit)
        self.mode = ModeType(mode)

        self.analysis_func = self.analysis.analysis_func

    def get_description(self, final):
        # TODO: assert that `final` is a valid pitch class
        return (
            f"{self.analysis.description}, {self.repertoire_and_genre.description}, {self.mode.get_description(final)}"
        )

    def __repr__(self):
        return (
            f"<FullAnalysisSpec: "
            f"repertoire_and_genre={self.repertoire_and_genre.value!r}, "
            f"analysis={self.analysis.value!r}, "
            f"unit={self.unit.value!r}, "
            f"mode={self.mode.value!r}, "
            ">"
        )

    def output_path(self, *, root_dir):
        return os.path.join(
            root_dir,
            self.repertoire_and_genre.path_stub_1,
            self.analysis.value,
            self.repertoire_and_genre.path_stub_2,
            self.unit.value,
            self.mode.value,
        )

    def export_results(self, *, output_root_dir, group, p_cutoff):
        assert isinstance(group, ModalCategory)
        output_dir = self.output_path(root_dir=output_root_dir)
        df = group.make_results_dataframe(analysis_func=self.analysis_func)
        dendrogram = Dendrogram(df, p_threshold=p_cutoff)
        if not os.path.exists(output_dir):
            print(f"Creating output dir: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)

        final = group.key
        output_filename = os.path.join(output_dir, "dendrogram.png")
        title = f"Dendrogram: {self.get_description(final)}"
        fig = dendrogram.plot_dendrogram(title=title)
        fig.savefig(output_filename)
        print(f"Saved dendrogram plot: '{output_filename}'")

        output_filename = os.path.join(output_dir, "stacked_bar_chart.png")
        title = self.get_description(final)
        fig = dendrogram.plot_stacked_bar_charts(title=title)
        fig.savefig(output_filename)
        print(f"Saved stacked bar chart: '{output_filename}'")
