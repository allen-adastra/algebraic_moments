import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path + "/../")
from objects import RandomVariable, RandomVector
from moment_form import generate_moment_constraints

def test_foo():
    x = RandomVariable("x")
    y = RandomVariable("y")
    vector = RandomVector([x, y], [])
    expressions = [(x*y**2 + y)**2, (y*x**2 + y**2)**3]
    generate_moment_constraints(expressions, vector, "matlab")