from .utils import EnumWithDescription

__all__ = ["UnitType"]


class UnitType(EnumWithDescription):
    PCS = ("pcs", "pitch classes")
    MODE_DEGREES = ("mode_degrees", "mode degrees")

    @property
    def output_path_stub(self):
        if self.value == "pcs":
            return "1_pcs"
        elif self.value == "mode_degrees":
            return "2_mode_degrees"
        else:
            raise ValueError(f"Unexpected unit: '{self.value}'")

    @property
    def plot_title_descr(self):
        if self.value == "pcs":
            return "PCs: "
        elif self.value == "mode_degrees":
            return "MDs: "
        else:
            raise ValueError(f"Unexpected unit: '{self.value}'")
