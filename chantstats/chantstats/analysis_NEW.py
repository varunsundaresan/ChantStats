from .plainchant_sequence_monomodal_sections import extract_monomodal_sections

__all__ = ["prepare_analysis_inputs"]


def prepare_analysis_inputs(repertoire_and_genre, mode, *, cfg, min_length_monomodal_sections=3, filename_pattern=None):
    pieces = cfg.load_pieces(repertoire_and_genre, pattern=filename_pattern)

    if mode == "by_final":
        enforce_same_ambitus = False
    elif mode == "by_final_and_ambitus":
        enforce_same_ambitus = True
    else:
        raise NotImplementedError(f"Invalid mode: '{mode}'")

    if repertoire_and_genre == "plainchant_sequences":
        return extract_monomodal_sections(
            pieces, enforce_same_ambitus=enforce_same_ambitus, min_length=min_length_monomodal_sections
        )
    else:
        raise NotImplementedError(f"Unsupported repertoire/genre: {repertoire_and_genre}")
