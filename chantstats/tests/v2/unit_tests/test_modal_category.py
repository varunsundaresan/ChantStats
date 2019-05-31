import pandas as pd
from pandas.util.testing import assert_frame_equal
from music21.note import Note
from unittest.mock import Mock
from .context import chantstats
from chantstats.v2.pitch_class import PC
from chantstats.v2.modal_category import ModalCategoryType, ModalCategory, GroupingByModalCategory


class FakePiece:
    def __init__(self, final, ambitus="undefined", notes=None, descr=None):
        self.final = final
        self.ambitus = ambitus
        self.notes = notes
        self.descr = descr


def test_modal_category_type():
    t = ModalCategoryType("final")
    assert "final" == ModalCategoryType.FINAL == t
    assert t.enforce_same_ambitus == False
    assert t.get_output_path_stub_1("A") == "by_final"
    assert t.get_output_path_stub_2("A") == "6.A_1.final"
    assert t.get_descr("A") == "A-final"
    assert t.grouping_func(Mock(final="D")) == "D"

    t = ModalCategoryType("final_and_ambitus")
    assert "final_and_ambitus" == ModalCategoryType.FINAL_AND_AMBITUS == t
    assert t.enforce_same_ambitus == True

    assert t.get_output_path_stub_1(("B-", "plagal")) == "plagal_modes"
    assert t.get_output_path_stub_2(("B-", "plagal")) == "7.B-_3.plagal"
    assert t.get_descr(("B-", "plagal")) == "B--plagal"
    assert t.grouping_func(Mock(final="G", ambitus="plagal")) == ("G", "plagal")

    assert t.get_output_path_stub_1(("C", "authentic")) == "authentic_modes"
    assert t.get_output_path_stub_2(("C", "authentic")) == "9.C_2.authentic"
    assert t.get_descr(("C", "authentic")) == "C-authentic"
    assert t.grouping_func(Mock(final="F", ambitus="authentic")) == ("F", "authentic")


def test_grouping_by_modal_category():
    piece1 = FakePiece(final="G")
    piece2 = FakePiece(final="A")
    piece3 = FakePiece(final="B-")
    piece4 = FakePiece(final="G")
    piece5 = FakePiece(final="G")
    piece6 = FakePiece(final="A")

    # we use reverse order in the list of items to check that order is preserved in the resulting groups
    items = [piece6, piece5, piece4, piece3, piece2, piece1]
    grouping = GroupingByModalCategory(items, group_by="final")
    assert grouping["G"].items == [piece5, piece4, piece1]
    assert grouping["A"].items == [piece6, piece2]
    assert grouping["B-"].items == [piece3]

    piece1 = FakePiece(final="G", ambitus="authentic")
    piece2 = FakePiece(final="A", ambitus="plagal")
    piece3 = FakePiece(final="B-", ambitus="plagal")
    piece4 = FakePiece(final="G", ambitus="plagal")
    piece5 = FakePiece(final="G", ambitus="authentic")
    piece6 = FakePiece(final="A", ambitus="authentic")
    piece7 = FakePiece(final="B-", ambitus="plagal")

    # we use reverse order in the list of items to check that order is preserved in the resulting groups
    items = [piece7, piece6, piece5, piece4, piece3, piece2, piece1]
    grouping = GroupingByModalCategory(items, group_by="final_and_ambitus")
    assert grouping[("G", "authentic")].items == [piece5, piece1]
    assert grouping[("G", "plagal")].items == [piece4]
    assert grouping[("A", "authentic")].items == [piece6]
    assert grouping[("A", "plagal")].items == [piece2]
    assert grouping[("B-", "plagal")].items == [piece7, piece3]


def test_make_results_dataframe():
    notes1 = [Note("A3"), Note("D3"), Note("C3"), Note("D3"), Note("E3")]
    notes2 = [Note("F3"), Note("A3"), Note("G3"), Note("B-3"), Note("F3"), Note("C3"), Note("F3"), Note("B3")]
    notes3 = [Note("F3"), Note("C3"), Note("A3"), Note("G3"), Note("A3")]
    piece1 = FakePiece(descr="piece_1", final="G", notes=notes1)
    piece2 = FakePiece(descr="piece_2", final="G", notes=notes2)
    piece3 = FakePiece(descr="piece_3", final="G", notes=notes3)
    items = [piece3, piece2, piece1]
    modal_category = ModalCategory(items, modal_category_type="final", key="G")

    from chantstats.v2.freqs import PCFreqs

    def calculate_relative_pc_freqs(item, unit):
        return PCFreqs.from_notes(item.notes).rel_freqs

    df = modal_category.make_results_dataframe(analysis_func=calculate_relative_pc_freqs, unit="pcs")

    row_piece1 = pd.Series([40.0, 0, 20.0, 0, 0, 20.0, 0, 0, 20.0], index=list(PC))
    row_piece2 = pd.Series([0, 0, 0, 37.5, 12.5, 12.5, 12.5, 12.5, 12.5], index=list(PC))
    row_piece3 = pd.Series([0, 0, 0, 20.0, 20.0, 40.0, 0, 0, 20.0], index=list(PC))
    df_expected = pd.DataFrame({"piece_3": row_piece3, "piece_2": row_piece2, "piece_1": row_piece1}).T
    assert_frame_equal(df_expected, df)
