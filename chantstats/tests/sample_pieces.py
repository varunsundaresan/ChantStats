import os
from chantstats.piece import PlainchantSequencePiece

try:
    chants_dir = os.environ["CHANTS_DIR"]
except KeyError:
    raise RuntimeError("The environment variable CHANTS_DIR must be defined to run the tests.")

#
# Load sample pieces
#
piece1 = PlainchantSequencePiece(os.path.join(chants_dir, "01_Salus_eterna.xml"))       # monomodal frame (no amen formula)
piece2 = PlainchantSequencePiece(os.path.join(chants_dir, "02_Regnantem.xml"))          # monomodal frame (with amen formula)
piece3 = PlainchantSequencePiece(os.path.join(chants_dir, "03_Qui_regis.xml"))          # heavy polymodal frame 1 (no amen formula)
piece4 = PlainchantSequencePiece(os.path.join(chants_dir, "04_Iubilemus_omnes.xml"))    # heavy polymodal frame 1 (no amen formula)
piece5 = PlainchantSequencePiece(os.path.join(chants_dir, "05_Letabundus.xml"))         # monomodal frame (with amen formula)
piece6 = PlainchantSequencePiece(os.path.join(chants_dir, "06_Hac_clara_die.xml"))      # heavy polymodal frame 1 (no amen formula)
piece7 = PlainchantSequencePiece(os.path.join(chants_dir, "07_Splendor_patris.xml"))    # monomodal frame (with amen formula)
piece8 = PlainchantSequencePiece(os.path.join(chants_dir, "08_In_excelsis_canitur.xml"))  # monomodal frame (without amen formula)
piece12 = PlainchantSequencePiece(os.path.join(chants_dir, "12_Fulgens_preclara.xml"))  # heavy polymodal frame 1 (no amen formula)
piece14 = PlainchantSequencePiece(os.path.join(chants_dir, "14_Zima_uetus.xml"))        # light polymodal frame 1 (with amen formula)
piece45 = PlainchantSequencePiece(os.path.join(chants_dir, "45_Aue_maria_gratia_plena.xml"))  # light polymodal frame 2 (with amen formula)