from algebraic_moments.objects import Moment, RandomVariable, RandomVector, DeterministicVariable
from algebraic_moments.generate_inequality import generate_concentration_inequality
from sympy.matrices import Matrix

def cantelli():
    """ Given the random vector g = [gx, gy]^T, rotation matrix R, and psd matrix Q,
        generate code to bound:
            P((Rg)^T Q (Rg) <= 0)
        Using Cantelli's inequality.
    """

    # The random vector.
    gx = RandomVariable("gx")
    gy = RandomVariable("gy")
    pairwise_dependence = [(gx, gy)] # Assume gx and gy are pairwise dependent
    random_vec = RandomVector([gx, gy], pairwise_dependence)

    # Deterministic variables defining the rotation.
    c = DeterministicVariable("c")
    s = DeterministicVariable("s")
    R = Matrix([[c, -s], [s, c]])

    # Define the Q matrix.
    q1 = DeterministicVariable("q1")
    q2 = DeterministicVariable("q2")
    q3 = DeterministicVariable("q3")
    Q = Matrix([[q1, q2],[q2, q3]])

    # List all deterministic variables.
    deterministic_vars = [c, s, q1, q2, q3]

    # Express (Rg)^T Q (Rg)
    vec = Matrix([[gx], [gy]])
    rotated_vec = R.transpose() * vec
    collision_rv = rotated_vec.transpose() * Q * rotated_vec
    collision_rv = collision_rv[0,0]

    # Generate the code for the concentration inequality.
    concentration_inequality = generate_concentration_inequality(collision_rv, random_vec, deterministic_vars, "cantelli")
    concentration_inequality.print("python")

cantelli()