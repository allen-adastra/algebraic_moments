from algebraic_moments.objects import Moment, RandomVariable, RandomVector, DeterministicVariable
from algebraic_moments.moment_expressions import generate_moment_expressions
from sympy.matrices import Matrix

def transform_frames():
    """ Given the random vector [gx, gy]^T, transform its moments into the frame
        centered at [x, y]^T and rotated by theta degrees.
    """

    # The random vector.
    gx = RandomVariable("gx")
    gy = RandomVariable("gy")
    pairwise_dependence = [(gx, gy)] # Assume gx and gy are pairwise dependent
    random_vec = RandomVector([gx, gy], pairwise_dependence)

    # Deterministic variables defining the new frame.
    c = DeterministicVariable("c")
    s = DeterministicVariable("s")
    deterministic_vars = [c, s]

    # Use the SymPy matrix class to perform the transformation
    # to get the transformed x and y, tx and ty.
    R = Matrix([[c, -s], [s, c]])
    vec = Matrix([[gx], [gy]])
    transformed = R.transpose() * vec
    tx = transformed[0]
    ty = transformed[1]

    # Now we want the following moments of tx and ty.
    desired_moments = {"txPow1" : tx, "tyPow1" : ty, "txPow2" : tx**2, "tyPow2" : ty**2, "tx_ty" : tx*ty, "txPow4" : tx**4}
    moment_expressions = generate_moment_expressions(desired_moments, random_vec, deterministic_vars)
    moment_expressions.print("matlab")

transform_frames()