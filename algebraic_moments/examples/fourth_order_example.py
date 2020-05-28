from algebraic_moments.objects import Moment, RandomVariable, RandomVector, DeterministicVariable
from algebraic_moments.generate_inequality import generate_moment_expressions
from sympy.matrices import Matrix

def fourth_order_collision_rv_moments():
    """
    """

    # Declare the random vector.
    x = RandomVariable("x")
    y = RandomVariable("y")
    pairwise_dependence = [(x, y)]
    random_vec = RandomVector([x, y], pairwise_dependence)

    # Express the collision random variable.
    q11 = DeterministicVariable("q11")
    q12 = DeterministicVariable("q12")
    q22 = DeterministicVariable("q22")
    Q = Matrix([[q11, q12],[q12, q22]])
    deterministic_variables = [q11, q12, q22]
    vec = Matrix([[x], [y]])
    Qrv = vec.transpose() * Q * vec
    Collisionrv = Qrv[0, 0] - 1

    # Express moments of the collision random variable.
    expressions = {"CollisionrvPow1" : Collisionrv, "CollisionrvPow2" : Collisionrv**2,\
                   "CollisionrvPow3" : Collisionrv**3, "CollisionrvPow4" : Collisionrv**4}
    moment_expressions = generate_moment_expressions(expressions, random_vec, deterministic_variables)

    moment_expressions.print_python(multi_idx_keys = False)
    moment_expressions.print_python(multi_idx_keys = True)

fourth_order_collision_rv_moments()