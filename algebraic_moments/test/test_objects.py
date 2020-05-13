import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path + "/../")
from objects import RandomVariable, RandomVector, Moment

def test_RandomVariable():
    w = RandomVariable("w")
    x = RandomVariable("x")

    # Test that multiplication produces the correst string.
    assert str(w*x) == "w*x"

def test_RandomVector():
    w = RandomVariable("w")
    x = RandomVariable("x")
    rv = RandomVector([w, x], [])
    assert rv.vpm((1, 2)) == {w : 1, x : 2}

def test_Moment():
    w = RandomVariable("w")
    x = RandomVariable("x")

    # The order of the vpms should not affect equality.
    m1 = Moment.from_vpm({w: 1, x: 3})
    m2 = Moment.from_vpm({x: 3, w : 1})
    assert m1.same_vpm(m2)
    assert str(m1) == "w1_x3"
    assert str(m2) == "x3_w1" # TODO: enforce an ordering of variable names

    # m1 should not equal another moment with a different vpm.
    m3 = Moment.from_vpm({w : 2, x : 3})
    assert m3.same_vpm(m1) == False