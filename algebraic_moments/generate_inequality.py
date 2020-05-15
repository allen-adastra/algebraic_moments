from algebraic_moments.moment_expressions import generate_moment_expressions
from algebraic_moments.objects import ConcentrationInequalityType, ConcentrationInequality

def generate_concentration_inequality(constraint_rv_expression, random_vec,
                                      deterministic_vars, inequality_type):
    """ Consider Prob(g(x, w) <= 0) where g is polynomial, x is a deterministic
        vector, and w is a random vector, this function generates code to upper
        bound the probability via a concentration inequality. It expresses
        the required mean and variance of g(x, w) in terms of x and moments of w.

    Args:
        constraint_rv (constraint_rv_expression): The constraint random variable p(w)
        random_vec (RandomVector): The random vector w
        deterministic_vars (list of DeterministicVariable): deterministic variables in the expression constraint_rv
        inequality_type (string) : Concentration inequality to generate
    """
    expressions = {"first_moment" : constraint_rv_expression, "second_moment" : constraint_rv_expression**2}
    moment_expressions = generate_moment_expressions(expressions, random_vec, deterministic_vars)
    if inequality_type == "cantelli":
        return ConcentrationInequality(moment_expressions, ConcentrationInequalityType.CANTELLI)
    elif inequality_type == "vp":
        return ConcentrationInequality(moment_expressions, ConcentrationInequalityType.VP)
    elif inequality_type == "gauss":
        return ConcentrationInequality(moment_expressions, ConcentrationInequalityType.GAUSS)
    else:
        raise Exception("Invalid inequality type input.")