from itertools import count

import numpy as np

from chantstats import GroupingByModalCategory
from chantstats.pitch_class_freqs import PCFreqs

pcs = ["A", "B", "C", "D", "E", "F", "G"]


class DummyItem:
    counter = count(start=1)

    def __init__(self, *, final, ambitus, index=None):
        self.index = index or next(self.counter)
        self.descr = f"DummyItem #{self.index}"
        self.final = final
        self.ambitus = ambitus
        self.random_state = np.random.RandomState()
        self.random_state.seed(self.index)
        self.pitch_classes = list(self.random_state.choice(pcs, size=100))
        self.pc_freqs = PCFreqs(self.pitch_classes)

    def __repr__(self):
        return f"<DummyItem #{self.index!r}: final={self.final!r}, ambitus={self.ambitus!r}>"


def make_dummy_items(*, final, ambitus, num):
    return [DummyItem(final=final, ambitus=ambitus) for _ in range(num)]


dummy_items = sum(
    [
        make_dummy_items(final="C", ambitus="authentic", num=5),
        make_dummy_items(final="D", ambitus="authentic", num=10),
        make_dummy_items(final="D", ambitus="plagal", num=12),
        make_dummy_items(final="G", ambitus="authentic", num=20),
        make_dummy_items(final="G", ambitus="plagal", num=18),
    ],
    [],
)


def make_dummy_grouping_by_modal_category(*, group_by):
    return GroupingByModalCategory(dummy_items, group_by=group_by)
