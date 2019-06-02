from .helpers import pairwise
from ..note_pair import NotePair

# from .melodic_outlines import calculate_melodic_outline_candidates
# from .pc_pair_condprobs import PCPairCondProbs


class OrganumPhrase:
    def __init__(self, df, piece_filename):
        self.df = df
        self.piece_filename = piece_filename
        self._run_sanity_checks()

    def _run_sanity_checks(self):
        texture = list(self.df[("common", "texture")].unique())
        assert texture == ["organum_purum"], "Phrases are only defined for organum purum sections"

    @property
    def _measure_descr(self):
        measures = self.df[("common", "measure")].unique()
        if len(measures) == 1:
            return "measure {}".format(measures[0])
        else:
            return "measures {}-{}".format(measures[0], measures[-1])

    def __repr__(self):
        return "<OrganumPhrase of length {} on tenor PC '{}', piece '{}', contained in {}>".format(
            len(self.pitch_classes), self.tenor_pc, self.piece_filename, self._measure_descr
        )

    def __len__(self):
        return len(self.pitch_classes)

    @property
    def tenor_pc(self):
        tenor_pcs = self.df[("tenor", "pitch_class")].dropna().unique()
        assert len(tenor_pcs) == 1, "[DDD] Missing or non-unique tenor PC: tenor_pcs={}, piece={}, df={}".format(
            tenor_pcs, self.piece_filename, self.df
        )
        return tenor_pcs[0]

    @property
    def pitch_classes(self):
        duplum_pcs = self.df[("duplum", "pitch_class")]
        if any(duplum_pcs.isnull()):
            raise RuntimeError("Some duplum notes in organum phrase are null: {}".format(duplum_pcs))
        return list(duplum_pcs)

    @property
    def notes(self):
        duplum_notes = self.df[("duplum", "note")]
        if any(duplum_notes.isnull()):
            raise RuntimeError("Some duplum notes in organum phrase are null: {}".format(duplum_notes))
        return list(duplum_notes)

    @property
    def pitch_class_pairs(self):
        return pairwise(self.pitch_classes)

    @property
    def note_pairs(self):
        # return pairwise(self.notes)
        return [NotePair(n1, n2) for n1, n2 in pairwise(self.notes)]

    def get_note_pairs_with_interval(self, interval_name):
        return [note_pair for note_pair in self.note_pairs if note_pair.interval.name == interval_name]

    # @property
    # def pc_pair_condprobs(self):
    #     return PCPairCondProbs.from_seq(self.pitch_classes)

    # @property
    # def melodic_outlines(self):
    #     yield from [mo for mo in calculate_melodic_outline_candidates(self) if mo.is_proper_melodic_outline]
