from .context import chantstats
from chantstats.v2.modal_category import ModalCategory
from chantstats.v2.result_descriptor import ResultDescriptor


def test_result_descriptor():
    output_root_dir = "/tmp/foo/"
    modal_category = ModalCategory(items=None, modal_category_type="final", key="G")
    rd = ResultDescriptor("plainchant_sequences", "pc_freqs", "pcs", modal_category)
    assert rd.output_dirname == "chant/pc_freqs/sequences/pcs"
    assert rd.get_output_dir(output_root_dir) == "/tmp/foo/chant/pc_freqs/sequences/pcs"
    assert rd.get_output_dir(output_root_dir) == "/tmp/foo/chant/pc_freqs/sequences/pcs"
    assert (
        rd.get_full_output_path(output_root_dir, filename_prefix="dendrogram", filename_suffix="")
        == "/tmp/foo/chant/pc_freqs/sequences/pcs/dendrogram__5.G_1.final.png"
    )
    assert (
        rd.get_full_output_path(output_root_dir, filename_prefix="quux", filename_suffix="")
        == "/tmp/foo/chant/pc_freqs/sequences/pcs/quux__5.G_1.final.png"
    )

    output_root_dir = "/quux/bar"
    modal_category = ModalCategory(items=None, modal_category_type="final_and_ambitus", key=("C", "plagal"))
    rd = ResultDescriptor("plainchant_sequences", "tendency", "mode_degrees", modal_category)
    assert rd.output_dirname == "chant/tendency/sequences/mode_degrees"
    assert (
        rd.get_full_output_path(output_root_dir, filename_prefix="dendrogram", filename_suffix="")
        == "/quux/bar/chant/tendency/sequences/mode_degrees/dendrogram__9.C_3.plagal.png"
    )
    assert (
        rd.get_full_output_path(output_root_dir, filename_prefix="foobar", filename_suffix="04")
        == "/quux/bar/chant/tendency/sequences/mode_degrees/foobar__9.C_3.plagal__04.png"
    )


def test_plot_title():
    modal_category = ModalCategory(items=None, modal_category_type="final", key="D")
    rd = ResultDescriptor("plainchant_sequences", "pc_freqs", "pcs", modal_category)
    assert rd.plot_title == "Chant: Analysis 1 Mode Profiles: Seq.: PCs: D-final"

    modal_category = ModalCategory(items=None, modal_category_type="final_and_ambitus", key=("G", "authentic"))
    rd = ResultDescriptor("responsorial_chants", "pc_freqs", "mode_degrees", modal_category)
    assert rd.plot_title == "Chant: Analysis 1 Mode Profiles: Resp.: MDs: G-authentic"

    modal_category = ModalCategory(items=None, modal_category_type="final_and_ambitus", key=("E", "authentic"))
    rd = ResultDescriptor("responsorial_chants", "tendency", "mode_degrees", modal_category)
    assert rd.plot_title == "Chant: Analysis 2 Tendency: Resp.: MDs: E-authentic"

    ## TODO: implement this!
    # modal_category = ModalCategory(items=None, modal_category_type="final_and_ambitus", key=("F", "plagal"))
    # rd = ResultDescriptor("responsorial_chants", "leaps_and_melodic_outlines", "mode_degrees", modal_category)
    # assert rd.plot_title == "Chant: Analysis 3 L&M: L5: Seq.: PCs: F-plagal"
    # assert rd.plot_title == "Chant: Analysis 3 L&M: L5&M5: Resp.: MDs: F-plagal"
