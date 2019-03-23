from .pitch_class_freqs import PCFreqs
from .plainchant_sequence_phrase import PlainchantSequencePhrase

__all__ = ["PhraseCollection"]


class PhraseCollection:
    """
    Represents a collection of phrases to which a particular analysis can be applied.
    """

    def __init__(self, phrases):
        if not all([isinstance(p, PlainchantSequencePhrase) for p in phrases]):  # pragma: no cover
            raise NotImplementedError(
                "TODO: This class should be agnostic of the type of input phrases it accepts. "
                "This warning only exists to ensure that this really is the case once we add "
                "support for pieces that are not of type PlainchantSequencePiece."
            )
        self.phrases = phrases

    @property
    def pc_freqs(self):
        return sum([p.pc_freqs for p in self.phrases], PCFreqs.zero_freqs)
