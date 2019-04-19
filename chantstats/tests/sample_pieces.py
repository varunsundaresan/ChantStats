import os
from chantstats import load_plainchant_sequence_pieces
from chantstats.plainchant_sequence_piece import PlainchantSequencePiece

try:
    chants_dir = os.environ["CHANTS_DIR"]
except KeyError:
    raise RuntimeError("The environment variable CHANTS_DIR must be defined to run the tests.")

#
# Load sample pieces
#
#  - piece1 has monomodal frame (no amen formula)
#  - piece2 has monomodal frame (with amen formula)
#  - piece3 has heavy polymodal frame 1 (no amen formula)
#  - piece4 has heavy polymodal frame 1 (no amen formula)
#  - piece5 has monomodal frame (with amen formula)
#  - piece6 has heavy polymodal frame 1 (no amen formula)
#  - piece7 has monomodal frame (with amen formula)
#  - piece8 has monomodal frame (without amen formula)
pieces_1_thru_8 = load_plainchant_sequence_pieces(chants_dir, pattern="BN_lat_1112_Sequence_0[1-8]*.xml")
piece1, piece2, piece3, piece4, piece5, piece6, piece7, piece8 = pieces_1_thru_8

prefix="BN_lat_1112_Sequence_"
piece12 = PlainchantSequencePiece(os.path.join(chants_dir, prefix+"12_Fulgens_preclara.xml"))        # heavy polymodal frame 1 (no amen formula)
piece14 = PlainchantSequencePiece(os.path.join(chants_dir, prefix+"14_Zima_uetus.xml"))              # light polymodal frame 1 (with amen formula)
piece32 = PlainchantSequencePiece(os.path.join(chants_dir, prefix+"32_Magnus_deus.xml"))             # heavy polymodal frame 2 (with amen formula)
piece45 = PlainchantSequencePiece(os.path.join(chants_dir, prefix+"45_Aue_maria_gratia_plena.xml"))  # light polymodal frame 2 (with amen formula)
