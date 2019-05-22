from .context import chantstats
from chantstats.v2.unit import UnitType


def test_unit_type():
    assert "pcs" == UnitType("pcs").output_path_stub
    assert "pitch classes" == UnitType("pcs").description
    assert "mode_degrees" == UnitType("mode_degrees").output_path_stub
    assert "mode degrees" == UnitType("mode_degrees").description
