from chantstats.utils import EnumWithDescription


class UnitType(EnumWithDescription):
    PCS = ("pcs", "pitch classes")
    MODE_DEGREES = ("mode_degrees", "mode degrees")

    @property
    def output_path_stub(self):
        return self.value
