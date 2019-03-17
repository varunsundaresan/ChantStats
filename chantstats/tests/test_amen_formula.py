from .sample_pieces import *


def test_amen_formula():
    assert piece1.has_amen_formula == False
    assert piece2.has_amen_formula == True
    assert piece3.has_amen_formula == False
    assert piece4.has_amen_formula == False
    assert piece5.has_amen_formula == True
    assert piece6.has_amen_formula == False
    assert piece7.has_amen_formula == True
    # assert piece8.has_amen_formula == False
    assert piece12.has_amen_formula == False
    assert piece14.has_amen_formula == True
    assert piece45.has_amen_formula == True
