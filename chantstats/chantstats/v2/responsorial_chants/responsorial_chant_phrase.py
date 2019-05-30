from ..base_phrase import BasePhrase

__all__ = ["ResponsorialChantPhrase"]


class ResponsorialChantPhrase(BasePhrase):
    """
    Represents a phrase in a plainchant sequence piece.
    """

    def __init__(self, measure_stream, *, piece):
        super().__init__(measure_stream, piece=piece)

    def __repr__(self):
        return f"<Resp. Phrase {self.phrase_number} of piece {self.piece}>"
