from .context import chantstats
from chantstats.modal_category import ModalCategory


def test_modal_category_output_path_stub():
    mc = ModalCategory(items=[], modal_category_type="final", key="D")
    assert mc.output_path_stub == "by_final/D_final"
    mc = ModalCategory(items=[], modal_category_type="final", key="G")
    assert mc.output_path_stub == "by_final/G_final"

    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("C", "authentic"))
    assert mc.output_path_stub == "authentic_modes/C_authentic"
    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("F", "authentic"))
    assert mc.output_path_stub == "authentic_modes/F_authentic"

    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("A", "plagal"))
    assert mc.output_path_stub == "plagal_modes/A_plagal"
    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("B", "plagal"))
    assert mc.output_path_stub == "plagal_modes/B_plagal"
