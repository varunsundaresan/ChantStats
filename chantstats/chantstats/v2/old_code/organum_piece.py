import music21
import os
import pandas as pd
import re
from music21.note import Note

from ..logging import logger
from ..melodic_outline import calculate_melodic_outline_candidates_for_phrase, get_melodic_outlines_from_candidates
from ..mode_degree import ModeDegree
from ..note_pair import NotePair
from ..pitch_class import PC
from .helpers import group_by_contiguous_values, pairwise
from .organum_piece_section import OrganumPieceSection
from .organum_phrase import OrganumPhrase


def warn_if_tenor_does_not_start_on_first_note_of_each_measure(df):
    df_first_row_of_each_group = df.groupby([("common", "measure")]).apply(lambda grp: grp.iloc[0])
    df_first_row_of_each_group = df_first_row_of_each_group[
        df_first_row_of_each_group[("common", "texture")] != "discant_or_copula"
    ]
    if df_first_row_of_each_group["tenor"].isnull().any().any():
        logger.warning(
            "There is a measure where the tenor does not start on the first note! Check if this causes problems..."
        )


def merge_series(s1, s2, dtype=None):
    """
    Merge two pandas series.

    If values at corresponding positions in s1, s2 are different from each other
    or if the result contains any null values then an error will be raised.
    """

    def merge_values(x, y):
        if pd.isnull(x):
            assert not pd.isnull(y)
            return y
        else:
            assert (x == y) or pd.isnull(y)
            return x

    result = s1.combine(s2, merge_values)
    if dtype:
        result = result.astype(dtype)
    return result


def is_single_measure(df):
    return len(df[("common", "measure")].unique()) == 1


def get_unique_column_value(df, col):
    vals = df[col].unique()
    assert len(vals) == 1, "Column value must be unique but got: {}".format(vals)
    return vals[0]


def has_compound_meter(df):
    assert is_single_measure(df)
    time_signature = get_unique_column_value(df, ("common", "time_signature"))
    compound_time_signature_pattern = "^[0-9]+/8$"
    if re.match(compound_time_signature_pattern, time_signature):
        return True
    else:
        return False


def get_texture(df):
    if has_compound_meter(df):
        return "discant_or_copula"
    elif df[("duplum", "note")].isnull().all():
        return "chant"
    else:
        return "organum_purum"


def add_texture(df):
    res = df.copy()
    res[("common", "texture")] = get_texture(df)
    return res


def calculate_dataframe_from_single_part_stream(stream):
    assert isinstance(stream, music21.stream.Part)

    def get_current_time_signature(note):
        return note.getContextByClass("TimeSignature").ratioString

    def get_lyric(note):
        return note.lyric if note.lyric is not None else ""

    def get_note_info(note):
        return (
            note.offset,
            note.name,
            # note.nameWithOctave,
            note,
            note.pitch.ps,
            note.duration.quarterLength,
            note.measureNumber,
            get_current_time_signature(note),
            get_lyric(note),
        )

    columns = ["offset", "pitch_class", "note", "pitch", "duration", "measure", "time_signature", "lyric"]
    df = pd.DataFrame([get_note_info(n) for n in stream.flat.notes], columns=columns)
    return df.set_index("offset")


def merge_corresponding_columns(df, colname, dtype=None):
    df[("common", colname)] = merge_series(df[("tenor", colname)], df[("duplum", colname)], dtype=dtype)
    del df[("tenor", colname)]
    del df[("duplum", colname)]


# TODO: to make things more efficient, avoid all this iteration over streams!
def get_stanza_boundary_offsets(stream):
    duplum_barlines = list(stream.parts[0].recurse(classFilter="Barline"))
    tenor_barlines = list(stream.parts[1].recurse(classFilter="Barline"))

    # sanity check that barlines in duplum and tenor parts coincide
    assert [(b.offset, b.style) for b in duplum_barlines] == [(b.offset, b.style) for b in tenor_barlines]

    barline_offsets = []
    for b in duplum_barlines:
        assert b.style in ["double", "final"], "Unexpected barline type: '{}' (measure: {})".format(
            b.style, b.measureNumber
        )
        if b.style == "final":
            offset = b.getOffsetInHierarchy(stream.parts[0])
            logger.debug("Found barline '{}' at offset {}, measure {}".format(b.style, offset, b.measureNumber))
            barline_offsets.append(offset)
    barline_offsets.insert(0, 0.0)

    return barline_offsets


def calculate_dataframe_from_music21_stream(stream, filename):
    """
    Given a music21 Stream, return a pandas DataFrame representing it.
    """
    assert len(stream.parts) == 2

    duplum = stream.parts[0]
    tenor = stream.parts[1]

    df_duplum = calculate_dataframe_from_single_part_stream(duplum)
    df_tenor = calculate_dataframe_from_single_part_stream(tenor)

    df = pd.concat([df_tenor, df_duplum], axis=1, keys=["tenor", "duplum"])
    merge_corresponding_columns(df, "measure", dtype=int)
    merge_corresponding_columns(df, "time_signature")

    # Sanity check for contiguous range of measures
    measures_expected = list(range(1, df[("common", "measure")].max() + 1))
    measures_found = list(df[("common", "measure")].unique())
    if measures_expected != measures_found:
        logger.warning(
            f"Dataframe for piece {filename} is missing measures between 1-{max(measures_expected)}: "
            f"{sorted(set(measures_expected).difference(measures_found))}"
        )

    # df['tenor'] = forward_fill_each_measure(df['tenor'])
    # assert not df[('tenor', 'measure')].isnull().any()
    # assert not df[('tenor', 'time_signature')].isnull().any()

    # df.groupby([('common', 'measure')]).apply(add_texture)
    # df[('common', 'texture')] = pd.concat([add_texture(x) for _, x in df.groupby([('common', 'measure')])])
    ggg = df.groupby([("common", "measure")])
    df = pd.concat([add_texture(x) for _, x in ggg], axis=0)

    #
    # Fill phrase numbers
    #
    df[("common", "phrase")] = None
    phrase_num = 0
    for _, df_grp in group_by_contiguous_values(df, ("common", "texture")):
        sec = OrganumPieceSection(df_grp, filename)
        for phrase in sec.phrases:
            phrase_num += 1
            df.loc[phrase.df.index, ("common", "phrase")] = phrase_num

    #
    # Calculate stanzas
    #
    stanza_boundary_offsets = get_stanza_boundary_offsets(stream)

    # sanity check that last barline was found at the end of the piece (after all notes)
    assert all(df.index < stanza_boundary_offsets[-1])

    df[("common", "stanza")] = None
    for stanza_num, (start_offset, end_offset) in enumerate(pairwise(stanza_boundary_offsets), start=1):
        # TODO: this raises a pandas warning because we're altering a copy; rewrite this in a safer way!
        df.loc[(start_offset <= df.index) & (df.index < end_offset), ("common", "stanza")] = stanza_num

    # verify that all entries have been assigned to some stanza
    assert not df[("common", "stanza")].isnull().any()

    df = df[["common", "tenor", "duplum"]]  # rearrange columns

    # TODO: this is just for sanity checking because it might cause us trouble
    warn_if_tenor_does_not_start_on_first_note_of_each_measure(df)

    # Check that the last measure has texture 'chant'
    assert df[("common", "texture")].iloc[-1] == "chant"

    return df


class OrganumPiece:
    def __init__(self, stream_or_filename):
        if isinstance(stream_or_filename, str):
            self.stream = music21.converter.parse(stream_or_filename)
            self.filename_full = os.path.abspath(stream_or_filename)
            self.filename_short = os.path.basename(stream_or_filename)
        # elif isinstance(stream_or_filename, music21.stream.Stream):
        #     self.stream = stream_or_filename
        #     self.filename_full = ""
        #     self.filename_short = ""
        else:  # pragma: no cover
            raise TypeError(f"Cannot load piece from object of type: '{type(stream_or_filename)}'")

        # TODO: extract stub_descr from filename
        self.descr_stub = re.match("^(F3.*)\.xml$", self.filename_short).group(1)

        self.df = calculate_dataframe_from_music21_stream(self.stream, self.filename_short)
        self.note_of_chant_final = self.df.iloc[-1]["tenor"]["note"]
        assert isinstance(self.note_of_chant_final, Note)
        self.note_of_final = self.note_of_chant_final  # alias
        self.chant_final = PC.from_note(self.note_of_final)
        self.final = self.chant_final  # alias

        self.duplum_notes = list(self.df[self.df["common", "texture"] == "organum_purum"]["duplum", "note"])
        if not all([isinstance(n, Note) for n in self.duplum_notes]):
            raise ValueError(f"duplum_notes contains non-note objects: {self.duplum_notes}")
        self.notes = self.duplum_notes  # alias for use in analysis function

        self.pitch_classes = [PC.from_note(n) for n in self.notes]
        self.mode_degrees = [ModeDegree.from_note_pair(note=n, base_note=self.note_of_final) for n in self.notes]
        self.pc_pairs = list(zip(self.pitch_classes, self.pitch_classes[1:]))
        self.note_pairs = [
            NotePair(n1, n2) for (n1, n2) in zip(self.notes, self.notes[1:])
        ]  # FIXME: calculate these from note_pairs in phrases!
        self.mode_degree_pairs = list(zip(self.mode_degrees, self.mode_degrees[1:]))
        self._melodic_outline_candidates = calculate_melodic_outline_candidates_for_phrase(self)

    def __repr__(self):
        return "<OrganumPiece: '{}'>".format(self.descr_stub)

    @property
    def descr(self):
        return self.filename_short

    @property
    def phrases(self):
        """
        Iterate over all phrases in this OrganumPiece
        """
        return [
            OrganumPhrase(df_phrase, self.filename_short)
            for _, df_phrase in self.df.dropna(subset=[("common", "phrase")]).groupby([("common", "phrase")])
        ]

    def get_note_pairs_with_interval(self, interval_name):
        return [x for x in self.note_pairs if x.is_interval(interval_name)]

    def get_melodic_outlines(self, interval_name, *, allow_thirds=False):
        return get_melodic_outlines_from_candidates(
            self._melodic_outline_candidates, interval_name, allow_thirds=allow_thirds
        )
