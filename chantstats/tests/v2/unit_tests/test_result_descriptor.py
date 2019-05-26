from .context import chantstats
from chantstats.v2.modal_category import ModalCategory
from chantstats.v2.result_descriptor import ResultDescriptor


def test_result_descriptor():
    output_root_dir = "/tmp/foo/"
    modal_category = ModalCategory(items=None, modal_category_type="final", key="G")
    rd = ResultDescriptor("plainchant_sequences", "pc_freqs", "pcs", modal_category)
    assert rd.output_dirname == "chant/pc_freqs/sequences/pcs"
    assert rd.get_output_dir(output_root_dir, p_cutoff=0.3) == "/tmp/foo/p_cutoff_0.30/chant/pc_freqs/sequences/pcs"
    assert rd.get_output_dir(output_root_dir, p_cutoff=0.4) == "/tmp/foo/p_cutoff_0.40/chant/pc_freqs/sequences/pcs"
    assert (
        rd.get_full_output_path(output_root_dir, "dendrogram.png", p_cutoff=0.2)
        == "/tmp/foo/p_cutoff_0.20/chant/pc_freqs/sequences/pcs/final_G|dendrogram.png"
    )
    assert (
        rd.get_full_output_path(output_root_dir, "quux.png", p_cutoff=0.6)
        == "/tmp/foo/p_cutoff_0.60/chant/pc_freqs/sequences/pcs/final_G|quux.png"
    )

    output_root_dir = "/quux/bar"
    modal_category = ModalCategory(items=None, modal_category_type="final_and_ambitus", key=("C", "plagal"))
    rd = ResultDescriptor("plainchant_sequences", "tendency", "mode_degrees", modal_category)
    assert rd.output_dirname == "chant/tendency/sequences/mode_degrees"
    assert (
        rd.get_full_output_path(output_root_dir, "dendrogram.png", p_cutoff=0.15)
        == "/quux/bar/p_cutoff_0.15/chant/tendency/sequences/mode_degrees/plagal_C|dendrogram.png"
    )
    assert (
        rd.get_full_output_path(output_root_dir, "foobar.png", p_cutoff=0.04)
        == "/quux/bar/p_cutoff_0.04/chant/tendency/sequences/mode_degrees/plagal_C|foobar.png"
    )
