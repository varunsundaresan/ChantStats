from ..base_phrase import BasePhrase

__all__ = ["ResponsorialChantPhrase"]


class ResponsorialChantPhrase(BasePhrase):
    """
    Represents a phrase in a plainchant sequence piece.
    """

    def __init__(self, measure_stream, *, piece):
        super().__init__(measure_stream, piece=piece)
        self.is_last_phrase_in_stanza = self._has_double_or_final_barline()

    def _has_double_or_final_barline(self):
        """
        Return True if this phrase ends in a double or final barline
        (these indicate stanza boundaries in responsorial chant pieces).
        """
        barlines = list(self.measure_stream.getElementsByClass("Barline"))
        assert len(barlines) <= 1
        assert all([b.style in ("double", "final") for b in barlines])
        return len(barlines) == 1

    def __repr__(self):
        return f"<Resp. Phrase {self.phrase_number} of piece {self.piece}>"
