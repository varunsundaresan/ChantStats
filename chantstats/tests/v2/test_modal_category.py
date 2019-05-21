from unittest.mock import Mock
from .context import chantstats
from chantstats.v2.modal_category import ModalCategoryType


def test_modal_category_type():
    t = ModalCategoryType("final")
    assert "final" == ModalCategoryType.FINAL == t
    assert t.enforce_same_ambitus == False
    assert t.get_output_path_stub_1("A") == "by_final"
    assert t.get_output_path_stub_2("A") == "A_final"
    assert t.get_descr("A") == "A-final"
    assert t.grouping_func(Mock(final="D")) == "D"

    t = ModalCategoryType("final_and_ambitus")
    assert "final_and_ambitus" == ModalCategoryType.FINAL_AND_AMBITUS == t
    assert t.enforce_same_ambitus == True

    assert t.get_output_path_stub_1(("E-", "plagal")) == "plagal_modes"
    assert t.get_output_path_stub_2(("E-", "plagal")) == "E-_plagal"
    assert t.get_descr(("E-", "plagal")) == "E--plagal"
    assert t.grouping_func(Mock(final="G", ambitus="plagal")) == ("G", "plagal")

    assert t.get_output_path_stub_1(("C", "authentic")) == "authentic_modes"
    assert t.get_output_path_stub_2(("C", "authentic")) == "C_authentic"
    assert t.get_descr(("C", "authentic")) == "C-authentic"
    assert t.grouping_func(Mock(final="F", ambitus="authentic")) == ("F", "authentic")
