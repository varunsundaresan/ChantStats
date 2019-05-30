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
        self.final = self.phrases[-1].final

    def __repr__(self):
        s = (
            f"<RespChantStanza: '{self.piece.filename_short}', "
            f"stanza-final '{self.final}', "
            f"phrases {self.idx_start}-{self.idx_end} "
            f"({self.num_phrases} phrases, {self.num_notes} notes), "
            # f"ambitus={self.ambitus.value!r}"
            f">"
        )
        return s
