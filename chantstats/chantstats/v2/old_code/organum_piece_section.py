from ..mode_degree import ModeDegree
from ..note_pair import NotePair
from ..pitch_class import PC
from .helpers import group_by_contiguous_values
from .organum_phrase import OrganumPhrase


class BaseOrganumPieceSection:
    """
    This is a helper class representing a section of an
    organum piece, i.e. a contiguous set of measures with
    the same texture (= organum purum, discant/copula or
    chant).
    """

    def __init__(self, df, piece_filename, piece_descr_stub):
        self.df = df

        texture_vals = self.df[("common", "texture")].unique()
        if len(texture_vals) != 1:
            raise ValueError("Section does not have a unique texture: {}".format(texture_vals))

        self.texture = texture_vals[0]
        self.piece_filename = piece_filename
        self.piece_descr_stub = piece_descr_stub

    @property
    def _measure_descr(self):
        measures = self.df[("common", "measure")].unique()
        if len(measures) == 1:
            return "measure {}".format(measures[0])
        else:
            return "measures {}-{}".format(measures[0], measures[-1])

    def __repr__(self):
        return "<Section of piece '{}': {}, texture '{}'>".format(
            self.piece_filename, self._measure_descr, self.texture
        )

    @property
    def phrases(self):
        """
        Iterate over all phrases in this Section. Note that phrases are only defined for
        organum purum sections, so for other textures this returns an empty list.
        """
        return []


class OrganumPieceOrganumPurumSection(BaseOrganumPieceSection):
    def __init__(self, df, piece_filename, piece_descr_stub, note_of_chant_final):
        super().__init__(df, piece_filename, piece_descr_stub)
        assert self.texture == "organum_purum"
        self.duplum_notes = list(self.df["duplum", "note"])
        self.notes = self.duplum_notes  # alias
        self.pitch_classes = [PC.from_note(n) for n in self.notes]
        self.mode_degrees = [ModeDegree.from_note_pair(note=n, base_note=note_of_chant_final) for n in self.notes]
        self.pc_pairs = list(zip(self.pitch_classes, self.pitch_classes[1:]))
        self.note_pairs = [NotePair(n1, n2) for (n1, n2) in zip(self.notes, self.notes[1:])]
        self.mode_degree_pairs = list(zip(self.mode_degrees, self.mode_degrees[1:]))

    @property
    def phrases(self):
        phrases = []
        tenor_ffilled = self.df["tenor"].ffill().dropna()
        for i, df_grp in group_by_contiguous_values(self.df, tenor_ffilled["note"]):
            phrases.append(OrganumPhrase(self.df.loc[df_grp.index], self.piece_filename, self.piece_descr_stub))
        return phrases


def OrganumPieceSection(df, piece_filename, piece_descr_stub, note_of_chant_final):
    texture_vals = df[("common", "texture")].unique()
    if len(texture_vals) != 1:
        raise ValueError("Section does not have a unique texture: {}".format(texture_vals))
    texture = texture_vals[0]

    if texture == "organum_purum":
        return OrganumPieceOrganumPurumSection(df, piece_filename, piece_descr_stub, note_of_chant_final)
    else:
        return BaseOrganumPieceSection(df, piece_filename, piece_descr_stub)
