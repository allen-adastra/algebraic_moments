from algebraic_moments.objects import Moment, RandomVariable, RandomVector, DeterministicVariable
from algebraic_moments.moment_form import generate_moment_constraints
from sympy.matrices import Matrix

def transform_frames():
    """ Given the random vector [gx, gy]^T, transform its moments into the frame
        centered at [x, y]^T and rotated by theta degrees.
    """

    # Deterministic variables defining the new frame.
    x = DeterministicVariable("x")
    y = DeterministicVariable("y")
    c = DeterministicVariable("cos(theta)")
    s = DeterministicVariable("sin(theta)")
    deterministic_vars = [x, y, c, s]

    # The random vector.
    gx = RandomVariable("gx")
    gy = RandomVariable("gy")
    pairwise_dependence = [(gx, gy)] # Assume gx and gy are pairwise dependent
    random_vec = RandomVector([gx, gy], pairwise_dependence)

    # Use the SymPy matrix class to perform the transformation
    # to get the transformed x and y, tx and ty.
    R = Matrix([[c, -s], [s, c]])
    vec = Matrix([[gx - x], [gy - y]])
    transformed = R.transpose() * vec
    tx = transformed[0]
    ty = transformed[1]

    # Now we want the following moments of tx and ty.
    desired_moments = [tx, ty, tx**2, ty**2, tx*ty]
    generate_moment_constraints(desired_moments, random_vec, deterministic_vars, "matlab")

transform_frames()