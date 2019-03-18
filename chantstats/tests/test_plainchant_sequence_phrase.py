from .sample_pieces import *


def test_time_signature():
    # Check time signatures in piece1
    assert "15/4" == piece1.phrases[0].time_signature  # measure has explicit time signature
    assert "15/4" == piece1.phrases[1].time_signature  # measure does not have explicit time signature
    assert "18/4" == piece1.phrases[2].time_signature  # measure has explicit time signature
    assert "18/4" == piece1.phrases[3].time_signature  # measure does not have explicit time signature
    assert "17/4" == piece1.phrases[4].time_signature  # measure has explicit time signature
    assert "17/4" == piece1.phrases[5].time_signature  # measure does not have explicit time signature
    assert "15/4" == piece1.phrases[6].time_signature  # measure has explicit time signature
    assert "22/4" == piece1.phrases[7].time_signature  # measure has explicit time signature
    assert "9/4" == piece1.phrases[8].time_signature  # measure has explicit time signature
    assert "8/4" == piece1.phrases[9].time_signature  # measure has explicit time signature
    assert "15/4" == piece1.phrases[10].time_signature  # measure has explicit time signature
    assert "27/4" == piece1.phrases[11].time_signature  # measure has explicit time signature

    # Check a few time signatures in piece45
    assert "13/4" == piece45.phrases[0].time_signature
    assert "13/4" == piece45.phrases[1].time_signature
    assert "14/4" == piece45.phrases[2].time_signature
    assert "20/4" == piece45.phrases[3].time_signature
    assert "41/4" == piece45.phrases[20].time_signature
    assert "5/4" == piece45.phrases[21].time_signature
