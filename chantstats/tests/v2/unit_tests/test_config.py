import pytest

from .context import chantstats
from chantstats.v2 import ChantStatsConfig


def test_musicxml_paths(monkeypatch):
    monkeypatch.setenv("CHANTS_DIR", "/tmp/foobar")
    cfg = ChantStatsConfig.from_env()
    assert cfg.get_musicxml_path("plainchant_sequences") == "/tmp/foobar/BN_lat_1112_Sequences/musicxml"
    assert cfg.get_musicxml_path("responsorial_chants") == "/tmp/foobar/Organum_Chant_Files_MLO_II_III_IV/musicxml"


def test_env_var_unset(monkeypatch):
    monkeypatch.delenv("CHANTS_DIR", raising=False)
    with pytest.raises(RuntimeError, match="The environment variable CHANTS_DIR must be defined to run the tests."):
        ChantStatsConfig.from_env()
