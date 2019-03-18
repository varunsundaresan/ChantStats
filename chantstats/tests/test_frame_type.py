from .sample_pieces import *
from chantstats.piece import FrameType


def test_frame_type():
    assert piece1.frame_type == FrameType.MONOMODAL_FRAME
    assert piece2.frame_type == FrameType.MONOMODAL_FRAME
    assert piece3.frame_type == FrameType.HEAVY_POLYMODAL_FRAME_1
    assert piece4.frame_type == FrameType.HEAVY_POLYMODAL_FRAME_1
    assert piece5.frame_type == FrameType.MONOMODAL_FRAME
    assert piece6.frame_type == FrameType.HEAVY_POLYMODAL_FRAME_1
    assert piece7.frame_type == FrameType.MONOMODAL_FRAME
    assert piece8.frame_type == FrameType.MONOMODAL_FRAME
    assert piece12.frame_type == FrameType.HEAVY_POLYMODAL_FRAME_1
    assert piece14.frame_type == FrameType.LIGHT_POLYMODAL_FRAME_1
    assert piece45.frame_type == FrameType.LIGHT_POLYMODAL_FRAME_2
