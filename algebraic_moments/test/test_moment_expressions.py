from algebraic_moments.objects import RandomVariable, RandomVector, DeterministicVariable
from algebraic_moments.moment_expressions import generate_moment_expressions

def test_foo():
    x = RandomVariable("x")
    y = RandomVariable("y")
    c = DeterministicVariable("c")
    vector = RandomVector([x, y], [])
    expressions = [(c * x*y**2 + y)**2, (y*x**2 + c*y**2)**3]
    deterministic_variables = [c]
    moment_expressions = generate_moment_expressions(expressions, vector, deterministic_variables)
    moment_expressions.print("matlab")

test_foo()