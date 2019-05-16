import music21
import os
import re

from .responsorial_chant_phrase import ResponsorialChantPhrase

__all__ = ["ResponsorialChantPiece"]


class ResponsorialChantPiece:
    """
    Represents a responsorial chant piece.
    """

    def __init__(self, stream_or_filename):
        if isinstance(stream_or_filename, str):
            self.stream = music21.converter.parse(stream_or_filename)
            self.filename_full = os.path.abspath(stream_or_filename)
            self.filename_short = os.path.basename(stream_or_filename)
        # elif isinstance(stream_or_filename, music21.stream.Stream):
        #     self.stream = stream_or_filename
        #     self.filename_full = ""
        #     self.filename_short = ""
        else:  # pragma: no cover
            raise TypeError(f"Cannot load piece from object of type: '{type(stream_or_filename)}'")

        self.name = re.sub(
            r"\.xml$", "", re.sub("_", " ", self.filename_short)
        )  # remove .xml suffix and replace underscores with spaces
        self.stub = re.match(r"^(.*)_.*\.xml", self.filename_short).group(1)

        num_parts = len(self.stream.parts)
        if num_parts != 1:  # pragma: no cover
            raise ValueError(f"Piece must have exactly one tenor part. Found {num_parts} parts.")

        self.tenor = self.stream.parts[0]
        self.measures = [m for m in self.tenor.getElementsByClass("Measure")]
        self.phrases = [ResponsorialChantPhrase(m, piece=self) for m in self.measures]
        self.num_phrases = len(self.phrases)
        self.phrase_finals = [p.phrase_final for p in self.phrases]
        self.phrase_final_notes = [p.phrase_final_note for p in self.phrases]

    def __repr__(self):
        return f"<Piece '{self.filename_short}'>"

    @property
    def pc_freqs(self):  # pragma: no cover
        raise NotImplementedError(
            "The .pc_freqs attribute is not supported directly because different analyses "
            "require different pre-processing of pieces (such as omitting modulatory phrases). "
            "Therefore this pre-processing should be done first and only then should the "
            "PC frequencies be calculated."
        )
