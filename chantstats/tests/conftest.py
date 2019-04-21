import os
import pytest
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory

from .context import chantstats
from chantstats.utils import make_dummy_grouping_by_modal_category

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


@pytest.fixture(scope="session")
def dummy_grouping_by_final():
    return make_dummy_grouping_by_modal_category(group_by="final")


@pytest.fixture(scope="session")
def dummy_grouping_by_final_and_ambitus():
    return make_dummy_grouping_by_modal_category(group_by="final_and_ambitus")
