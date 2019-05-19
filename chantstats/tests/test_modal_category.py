from .context import chantstats
from chantstats.modal_category import ModalCategory

# from chantstats.results_export_OLD import export_dendrogram_and_stacked_bar_chart


def test_modal_category_output_path_stub():
    mc = ModalCategory(items=[], modal_category_type="final", key="D")
    assert mc.output_path_stub_1 == "by_final"
    assert mc.output_path_stub_2 == "D_final"
    assert mc.descr == "D-final"
    mc = ModalCategory(items=[], modal_category_type="final", key="G")
    assert mc.output_path_stub_1 == "by_final"
    assert mc.output_path_stub_2 == "G_final"
    assert mc.descr == "G-final"

    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("C", "authentic"))
    assert mc.output_path_stub_1 == "authentic_modes"
    assert mc.output_path_stub_2 == "C_authentic"
    assert mc.descr == "C-authentic"
    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("F", "authentic"))
    assert mc.output_path_stub_1 == "authentic_modes"
    assert mc.output_path_stub_2 == "F_authentic"
    assert mc.descr == "F-authentic"

    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("A", "plagal"))
    assert mc.output_path_stub_1 == "plagal_modes"
    assert mc.output_path_stub_2 == "A_plagal"
    assert mc.descr == "A-plagal"
    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("B", "plagal"))
    assert mc.output_path_stub_1 == "plagal_modes"
    assert mc.output_path_stub_2 == "B_plagal"
    assert mc.descr == "B-plagal"
