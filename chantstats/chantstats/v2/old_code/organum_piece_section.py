from .helpers import group_by_contiguous_values
from .organum_phrase import OrganumPhrase


class OrganumPieceSection:
    """
    This is a helper class representing a section of an
    organum piece, i.e. a contiguous set of measures with
    the same texture (= organum purum, discant/copula or
    chant).
    """

    def __init__(self, df, piece_filename):
        self.df = df

        texture_vals = self.df[("common", "texture")].unique()
        if len(texture_vals) != 1:
            raise ValueError("Section does not have a unique texture: {}".format(texture_vals))

        self.texture = texture_vals[0]
        self.piece_filename = piece_filename

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
        organum purum sections, so for other textures this returns an empty generator.
        """
        if self.texture != "organum_purum":
            return

        tenor_ffilled = self.df["tenor"].ffill().dropna()
        for i, df_grp in group_by_contiguous_values(self.df, tenor_ffilled["note"]):
            yield OrganumPhrase(self.df.loc[df_grp.index], self.piece_filename)
