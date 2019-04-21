import textwrap
from itertools import count

from .context import chantstats
from chantstats import FullAnalysisSpec
from chantstats.modal_category import ModalCategory
from chantstats.utils import list_directory_tree


def test_modal_category_output_path_stub():
    mc = ModalCategory(items=[], modal_category_type="final", key="D")
    assert mc.output_path_stub == "by_final/D_final"
    assert mc.descr == "D-final"
    mc = ModalCategory(items=[], modal_category_type="final", key="G")
    assert mc.output_path_stub == "by_final/G_final"
    assert mc.descr == "G-final"

    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("C", "authentic"))
    assert mc.output_path_stub == "authentic_modes/C_authentic"
    assert mc.descr == "C-authentic"
    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("F", "authentic"))
    assert mc.output_path_stub == "authentic_modes/F_authentic"
    assert mc.descr == "F-authentic"

    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("A", "plagal"))
    assert mc.output_path_stub == "plagal_modes/A_plagal"
    assert mc.descr == "A-plagal"
    mc = ModalCategory(items=[], modal_category_type="final_and_ambitus", key=("B", "plagal"))
    assert mc.output_path_stub == "plagal_modes/B_plagal"
    assert mc.descr == "B-plagal"


def test_export_results_for_modal_category(dummy_grouping_by_final, tmpdir):
    output_root_dir = str(tmpdir)
    print(f"[DDD] dummy_grouping_by_final: {dummy_grouping_by_final}")
    grp = dummy_grouping_by_final.groups["D"]
    analysis_spec = FullAnalysisSpec(repertoire_and_genre="plainchant_sequences", analysis="pc_freqs", unit="pcs")
    grp.export_dendrogram_and_stacked_bar_chart(
        analysis_spec=analysis_spec, output_root_dir=output_root_dir, p_cutoff=0.7, overwrite=True
    )
    dir_tree = list_directory_tree(output_root_dir)
    expected_dir_tree = textwrap.dedent(
        """\
        .
        └── chant
            └── pc_freqs
                └── sequences
                    └── pcs
                        └── by_final
                            └── D_final
                                ├── dendrogram.png
                                └── stacked_bar_chart.png

        6 directories, 2 files
        """
    )
    assert expected_dir_tree == dir_tree


def test_export_results_for_grouping_by_modal_category(dummy_grouping_by_final, tmpdir):
    output_root_dir = str(tmpdir)
    print(f"[DDD] dummy_grouping_by_final: {dummy_grouping_by_final}")
    analysis_spec = FullAnalysisSpec(repertoire_and_genre="plainchant_sequences", analysis="pc_freqs", unit="pcs")
    dummy_grouping_by_final.export_results(
        analysis_spec=analysis_spec, output_root_dir=output_root_dir, p_cutoff=0.7, overwrite=True
    )
    dir_tree = list_directory_tree(output_root_dir)
    expected_dir_tree = textwrap.dedent(
        """\
        .
        └── chant
            └── pc_freqs
                └── sequences
                    └── pcs
                        └── by_final
                            ├── C_final
                            │   ├── dendrogram.png
                            │   └── stacked_bar_chart.png
                            ├── D_final
                            │   ├── dendrogram.png
                            │   └── stacked_bar_chart.png
                            └── G_final
                                ├── dendrogram.png
                                └── stacked_bar_chart.png

        8 directories, 6 files
        """
    )
    assert expected_dir_tree == dir_tree
