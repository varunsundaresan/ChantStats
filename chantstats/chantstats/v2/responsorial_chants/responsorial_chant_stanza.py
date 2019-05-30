from ..ambitus import calculate_ambitus

__all__ = ["ResponsorialChantStanza", "NonmodulatoryResponsorialChantStanza"]


class NonmodulatoryResponsorialChantStanza:
    def __init__(self, piece, phrase_numbers):
        self.piece = piece
        self.phrase_numbers = phrase_numbers
        self.phrases = [self.piece.phrases[n - 1] for n in phrase_numbers]
        self.notes = sum([p.notes for p in self.phrases], [])
        self.num_phrases = len(self.phrases)
        self.num_notes = len(self.notes)
        self.note_of_final = self.phrases[-1].notes[-1]
        self.lowest_note = min(
            [p.lowest_note for p in self.phrases]
        )  # TODO: should this also consider modulatory phrases?!
        self.final = self.phrases[-1].final
        self.ambitus = calculate_ambitus(self)
        self.descr = f"{self.piece.descr_stub}.{self.final}.pp_{'.'.join([str(n) for n in self.phrase_numbers])}"

        self.pitch_classes = sum([p.pitch_classes for p in self.phrases], [])
        self.pc_pairs = sum([p.pc_pairs for p in self.phrases], [])
        self.note_pairs = sum([p.note_pairs for p in self.phrases], [])
        self.mode_degrees = sum([p.mode_degrees for p in self.phrases], [])
        self.mode_degree_pairs = sum([p.mode_degree_pairs for p in self.phrases], [])

    def __repr__(self):
        s = (
            f"<NonmodRespChantStanza: piece '{self.piece.descr_stub}', "
            f"stanza-final '{self.final}', "
            f"phrases: {self.phrase_numbers} "
            f"({self.num_phrases} phrases, {self.num_notes} notes), "
            # f"ambitus={self.ambitus.value!r}"
            f">"
        )
        return s

    def __lt__(self, other):
        return (self.piece.descr_stub, tuple(self.phrase_numbers)) < (
            other.piece.descr_stub,
            tuple(other.phrase_numbers),
        )

    def get_melodic_outlines(self, interval_name, *, allow_thirds=False):
        return sum([p.get_melodic_outlines(interval_name, allow_thirds=allow_thirds) for p in self.phrases], [])

    def get_note_pairs_with_interval(self, interval_name):
        return sum([p.get_note_pairs_with_interval(interval_name) for p in self.phrases], [])


class ResponsorialChantStanza:
    def __init__(self, piece, idx_start, idx_end):
        # assert isinstance(piece, ResponsorialChantPiece)
        self.piece = piece
        self.idx_start = idx_start
        self.idx_end = idx_end
        self.phrases = piece.phrases[idx_start - 1 : idx_end]
        self.notes = sum([p.notes for p in self.phrases], [])
        self.num_phrases = len(self.phrases)
        self.num_notes = len(self.notes)
        self.stanza_final = self.phrases[-1].final
        self.final = self.stanza_final  # alias

    def __repr__(self):
        s = (
            f"<RespChantStanza: piece '{self.piece.descr_stub}', "
            f"stanza-final '{self.final}', "
            f"phrases {self.idx_start}-{self.idx_end} "
            f"({self.num_phrases} phrases, {self.num_notes} notes), "
            # f"ambitus={self.ambitus.value!r}"
            f">"
        )
        return s

    def without_modulatory_phrases(self):
        phrase_numbers = [p.phrase_number for p in self.phrases if p.final == self.stanza_final]
        return NonmodulatoryResponsorialChantStanza(self.piece, phrase_numbers)
