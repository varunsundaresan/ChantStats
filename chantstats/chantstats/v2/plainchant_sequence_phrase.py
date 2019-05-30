from .base_phrase import BasePhrase

__all__ = ["PlainchantSequencePhrase"]


class PlainchantSequencePhrase(BasePhrase):
    """
    Represents a phrase in a plainchant sequence piece.
    """

    def __repr__(self):
        return f"<Seq. Phrase {self.phrase_number} of piece {self.piece}>"
