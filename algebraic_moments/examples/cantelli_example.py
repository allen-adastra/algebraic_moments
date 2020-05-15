from algebraic_moments.objects import Moment, RandomVariable, RandomVector, DeterministicVariable
from algebraic_moments.generate_inequality import generate_concentration_inequality
from sympy.matrices import Matrix

def cantelli():

    # The random vector.
    gx = RandomVariable("gx")
    gy = RandomVariable("gy")
    pairwise_dependence = [(gx, gy)] # Assume gx and gy are pairwise dependent
    random_vec = RandomVector([gx, gy], pairwise_dependence)

    # Deterministic variables defining the new frame.
    c = DeterministicVariable("c")
    s = DeterministicVariable("s")
    q1 = DeterministicVariable("q1")
    q2 = DeterministicVariable("q2")
    q3 = DeterministicVariable("q3")
    deterministic_vars = [c, s]


    R = Matrix([[c, -s], [s, c]])
    vec = Matrix([[gx], [gy]])
    rotated_vec = R.transpose() * vec
    Q = Matrix([[q1, q2],[q2, q3]])
    collision_rv = rotated_vec.transpose() * Q * rotated_vec
    collision_rv = collision_rv[0,0]
    concentration_inequality = generate_concentration_inequality(collision_rv, random_vec, deterministic_vars, "cantelli")
    concentration_inequality.print("python")
cantelli()