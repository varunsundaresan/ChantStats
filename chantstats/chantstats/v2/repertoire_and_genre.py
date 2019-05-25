from .utils import EnumWithDescription

__all__ = ["RepertoireAndGenreType"]


class RepertoireAndGenreType(EnumWithDescription):
    PLAINCHANT_SEQUENCES = ("plainchant_sequences", "Sequences", ("chant", "sequences"))
    RESPONSORIAL_CHANTS = ("responsorial_chants", "Responsorial Chants", ("chant", "responsorial_chants"))
    ORGANA = ("organa", "Organa", ("organum", ""))

    def __new__(cls, name, desc, output_path_stubs, **kwargs):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj._description = desc
        obj.output_path_stub_1 = output_path_stubs[0]
        obj.output_path_stub_2 = output_path_stubs[1]
        return obj
