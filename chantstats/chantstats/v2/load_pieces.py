from .plainchant_sequence_piece import PlainchantSequencePieces
from .responsorial_chants import ResponsorialChantPieces
from .old_code.organum_piece import OrganumPieces


def load_pieces(repertoire_and_genre, cfg, filename_pattern=None):
    if repertoire_and_genre == "plainchant_sequences":
        return PlainchantSequencePieces.from_musicxml_files(cfg, filename_pattern=filename_pattern)
    elif repertoire_and_genre == "responsorial_chants":
        return ResponsorialChantPieces.from_musicxml_files(cfg, filename_pattern=filename_pattern)
    elif repertoire_and_genre == "organum_pieces":
        return OrganumPieces.from_musicxml_files(cfg, filename_pattern=filename_pattern)
    else:
        raise NotImplementedError()
