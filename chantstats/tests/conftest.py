import numpy as np
import os
import pytest
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
from itertools import count

from .context import chantstats
from chantstats import GroupingByModalCategory
from chantstats.pitch_class_freqs import PCFreqs

here = os.path.dirname(os.path.abspath(__file__))


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False, help="run slow tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow option was provided in CLI: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture(scope="session")
def diff_reporter():
    diff_reporter_factory = GenericDiffReporterFactory()
    diff_reporter_factory.load(os.path.join(here, "approvaltests_diff_reporters.json"))
    return diff_reporter_factory.get_first_working()


pcs = ["A", "B", "C", "D", "E", "F", "G"]


class DummyItem:
    counter = count(start=1)

    def __init__(self, *, final, ambitus):
        self.index = next(self.counter)
        self.descr = f"DummyItem #{self.index}"
        self.final = final
        self.ambitus = ambitus
        self.pitch_classes = list(np.random.choice(pcs, size=100))
        self.random_state = np.random.RandomState()
        self.random_state.seed(self.index)
        self.pc_freqs = PCFreqs(self.pitch_classes)


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


@pytest.fixture(scope="session")
def dummy_grouping():
    return GroupingByModalCategory(dummy_items, group_by="final")
