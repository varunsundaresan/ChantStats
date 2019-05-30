import music21
import os
from .responsorial_chant_phrase import ResponsorialChantPhrase
from .responsorial_chant_stanza import ResponsorialChantStanza

__all__ = ["ResponsorialChantPiece"]


class ResponsorialChantPiece:
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

        # TODO: extract stub_descr from filename

        num_parts = len(self.stream.parts)
        if num_parts != 1:  # pragma: no cover
            raise ValueError(f"Piece must have exactly one tenor part. Found {num_parts} parts.")

        self.tenor = self.stream.parts[0]

        # TODO: should we actually extract phrases here if we might drop them later?!
        self.measures = list(self.tenor.getElementsByClass("Measure"))
        self.phrases = [ResponsorialChantPhrase(m, piece=self) for m in self.measures]
        self.num_phrases = len(self.phrases)

    def __repr__(self):
        return f"<Piece '{self.filename_short}'>"

    def get_stanzas(self):
        stanza_ends = [p.phrase_number for p in self.phrases if p.is_last_phrase_in_stanza]
        stanza_starts = [1] + [n + 1 for n in stanza_ends[:-1]]
        idx_of_last_phrase_in_piece = self.phrases[-1].phrase_number
        assert idx_of_last_phrase_in_piece in stanza_ends
        return [
            ResponsorialChantStanza(self, idx_start, idx_end)
            for (idx_start, idx_end) in zip(stanza_starts, stanza_ends)
        ]
