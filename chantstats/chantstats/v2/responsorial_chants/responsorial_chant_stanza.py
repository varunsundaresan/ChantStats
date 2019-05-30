class NonmodulatoryResponsorialChantStanza:
    def __init__(self, piece, phrase_numbers):
        self.piece = piece
        self.phrase_numbers = phrase_numbers
        self.phrases = [self.piece.phrases[n - 1] for n in phrase_numbers]
        self.notes = sum([p.notes for p in self.phrases], [])
        self.num_phrases = len(self.phrases)
        self.num_notes = len(self.notes)
        self.final = self.phrases[-1].final

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
