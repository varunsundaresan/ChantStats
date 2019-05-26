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
        rd.get_full_output_path(output_root_dir, "dendrogram.png")
        == "/tmp/foo/chant/pc_freqs/sequences/pcs/final_G__dendrogram.png"
    )
    assert (
        rd.get_full_output_path(output_root_dir, "quux.png")
        == "/tmp/foo/chant/pc_freqs/sequences/pcs/final_G__quux.png"
    )

    output_root_dir = "/quux/bar"
    modal_category = ModalCategory(items=None, modal_category_type="final_and_ambitus", key=("C", "plagal"))
    rd = ResultDescriptor("plainchant_sequences", "tendency", "mode_degrees", modal_category)
    assert rd.output_dirname == "chant/tendency/sequences/mode_degrees"
    assert (
        rd.get_full_output_path(output_root_dir, "dendrogram.png")
        == "/quux/bar/chant/tendency/sequences/mode_degrees/plagal_C__dendrogram.png"
    )
    assert (
        rd.get_full_output_path(output_root_dir, "foobar.png")
        == "/quux/bar/chant/tendency/sequences/mode_degrees/plagal_C__foobar.png"
    )
