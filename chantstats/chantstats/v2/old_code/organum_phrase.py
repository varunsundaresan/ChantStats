from music21.note import Note
from .helpers import pairwise
from ..ambitus import calculate_ambitus
from ..mode_degree import ModeDegree
from ..note_pair import NotePair
from ..pitch_class import PC

# from .melodic_outlines import calculate_melodic_outline_candidates
# from .pc_pair_condprobs import PCPairCondProbs


class OrganumPhrase:
    def __init__(self, df, piece_filename, piece_descr_stub):
        self.df = df
        self.piece_filename = piece_filename
        self.phrase_number = df["common", "phrase"].iloc[0]
        self._run_sanity_checks()

        tenor_notes = self.df["tenor", "note"].dropna().apply(lambda n: n.nameWithOctave).unique()
        tenor_pcs = self.df["tenor", "pitch_class"].dropna().unique()
        if len(tenor_notes) != 1 or len(tenor_pcs) != 1:
            raise RuntimeError(
                f"[DDD] Missing or non-unique tenor PC: tenor_notes={tenor_notes}, tenor_pcs={tenor_pcs}, piece={self.piece_filename}, df={self.df}"
            )
        self.tenor_note = Note(tenor_notes[0])
        self.tenor_pc = tenor_pcs[0]

        # FIXME: adding the attribute 'final' is a hack; instead, we should call it 'reference_pc'
        # and also add reference_pc attributes to the other analysis input classes
        self.final = self.tenor_pc
        self.note_of_final = self.tenor_note
        # self.notes = list(self.df["duplum", "note"])
        # self.pitch_classes = [PC.from_note(n) for n in self.notes]
        self.mode_degrees = [ModeDegree.from_note_pair(note=n, base_note=self.note_of_final) for n in self.notes]
        self.pc_pairs = list(zip(self.pitch_classes, self.pitch_classes[1:]))
        # self.note_pairs = [NotePair(n1, n2) for (n1, n2) in zip(self.notes, self.notes[1:])]
        self.mode_degree_pairs = list(zip(self.mode_degrees, self.mode_degrees[1:]))
        self.lowest_note = min(self.notes)

        self.ambitus = calculate_ambitus(self)

        if not df["common", "phrase"].isnull().any():
            # FIXME: the only reason the phrase numbers can be null here is because we use this class
            # when constructing the organum piece dataframe in calculate_dataframe_from_music21_stream().
            # The values should only be null the first time around, and should be non-null the second time.
            # However, this is really a hack and should be fixed properly.
            self.descr = f"{piece_descr_stub}.p{self.phrase_number:02d}.{self._measure_descr_short}"

    def _run_sanity_checks(self):
        texture = list(self.df[("common", "texture")].unique())
        assert texture == ["organum_purum"], "Phrases are only defined for organum purum sections"
        assert list(self.df["common", "phrase"].unique()) == [self.phrase_number]

    @property
    def _measure_descr(self):
        measures = self.df[("common", "measure")].unique()
        if len(measures) == 1:
            return "measure {}".format(measures[0])
        else:
            return "measures {}-{}".format(measures[0], measures[-1])

    @property
    def _measure_descr_short(self):
        measures = self.df[("common", "measure")].unique()
        if len(measures) == 1:
            return f"m{measures[0]:02d}"
        else:
            return f"m.{measures[0]:02d}-{measures[-1]:02d}"

    def __repr__(self):
        return "<OrganumPhrase #{} of length {} on tenor PC '{}', piece '{}', contained in {}>".format(
            self.phrase_number, len(self.pitch_classes), self.tenor_pc, self.piece_filename, self._measure_descr
        )

    def __len__(self):
        return len(self.pitch_classes)

    def __lt__(self, other):
        return (self.piece_filename, self.phrase_number) < (other.piece_filename, other.phrase_number)

    @property
    def pitch_classes(self):
        duplum_pcs = self.df[("duplum", "pitch_class")]
        if any(duplum_pcs.isnull()):
            raise RuntimeError("Some duplum notes in organum phrase are null: {}".format(duplum_pcs))
        return [PC(pc_name) for pc_name in duplum_pcs]

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
