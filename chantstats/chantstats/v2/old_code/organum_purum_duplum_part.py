from ..ambitus import calculate_ambitus
from ..mode_degree import ModeDegree
from ..pitch_class import PC
from ..melodic_outline import calculate_melodic_outline_candidates_for_phrase, get_melodic_outlines_from_candidates


class OrganumPurumDuplumPart:
    def __init__(self, piece):
        assert piece.__class__.__name__ == "OrganumPiece"
        self.piece = piece
        self.note_of_final = self.piece.note_of_final
        self.final = self.piece.final
        self.descr = self.piece.descr_stub
        self.sections = [s for s in self.piece.sections if s.texture == "organum_purum"]

        self.duplum_notes = sum([s.duplum_notes for s in self.sections], [])
        self.notes = self.duplum_notes  # alias for use in analysis function
        self.lowest_note = min(self.notes)
        self.pitch_classes = [PC.from_note(n) for n in self.notes]
        self.mode_degrees = [ModeDegree.from_note_pair(note=n, base_note=self.note_of_final) for n in self.notes]

        self.note_pairs = sum([s.note_pairs for s in self.sections], [])
        self.pc_pairs = sum([s.pc_pairs for s in self.sections], [])
        self.mode_degree_pairs = sum([s.mode_degree_pairs for s in self.sections], [])
        self._melodic_outline_candidates = calculate_melodic_outline_candidates_for_phrase(self)
        # self.ambitus = calculate_ambitus(self)

    def __repr__(self):
        return "<OrganumPurumDuplumPart of piece: '{}'>".format(self.piece.descr_stub)

    def __lt__(self, other):
        return self.piece.descr_stub < other.piece.descr_stub

    def get_melodic_outlines(self, interval_name, *, allow_thirds=False):
        return get_melodic_outlines_from_candidates(
            self._melodic_outline_candidates, interval_name, allow_thirds=allow_thirds
        )

    def get_note_pairs_with_interval(self, interval_name):
        return [x for x in self.note_pairs if x.is_interval(interval_name)]
