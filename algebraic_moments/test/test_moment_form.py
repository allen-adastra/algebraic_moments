from algebraic_moments.objects import RandomVariable, RandomVector, DeterministicVariable
from algebraic_moments.moment_form import generate_moment_constraints

def test_foo():
    x = RandomVariable("x")
    y = RandomVariable("y")
    c = DeterministicVariable("c")
    vector = RandomVector([x, y], [])
    expressions = [(c * x*y**2 + y)**2, (y*x**2 + c*y**2)**3]
    deterministic_variables = [c]
    generate_moment_constraints(expressions, vector, deterministic_variables, "matlab")

test_foo()