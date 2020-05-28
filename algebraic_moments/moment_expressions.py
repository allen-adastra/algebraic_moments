import sympy as sp
import numpy as np
import networkx as nx
from enum import Enum

from algebraic_moments.objects import Moment, MomentExpressions

def generate_moment_expressions(expressions, random_vector, deterministic_variables):
    """[summary]

    Args:
        expressions ([type]): [description]
        random_vector ([type]): [description]
        deterministic_variables ([type]): [description]
        language ([type]): [description]
    """
    moments = [] # List of generated moments.
    moment_expressions = dict()
    for name, exp in expressions.items():
        moment_expressions[name], new_moments = moment_expression(exp, random_vector, moments)
        moments += new_moments
    moment_expressions = MomentExpressions(moment_expressions, moments, random_vector, deterministic_variables)
    return moment_expressions

def moment_expression(expression, random_vector, moments, partial_reduction=None):
    """ Generate a moment expression and add new moments to "moments".

    Args:
        expression ([type]): [description]
        random_vector ([type]): [description]
        moments ([type]): [description]
        partial_reduction (set or None): set of variables that we want to reduce. If None, then reduce everything.
    Raises:
        Exception: [description]

    Returns:
        [type]: [description]
    """
    # Express "expression" as a polynomial in the random vector.
    raw_polynomial = sp.poly(expression, random_vector.variables)

    # List of terms.
    terms = []

    # New moments that are generated.
    new_moments = []
    for multi_index, coeff in raw_polynomial.terms():
        # Go through each term of the raw_polynomial to group coefficients and factor
        # moments.

        # Get the variable power map of this term
        term_vpm = random_vector.vpm(multi_index)

        # Factor everything based off independence.
        components = random_vector.dependence_graph.subgraph_components(list(term_vpm.keys()))

        if partial_reduction:
            # The components that are a subset of the partial reduction.
            factored_components = [comp for comp in components if set(comp).issubset(partial_reduction)]

            # The components that are not a subset of the partial reduction are grouped together.
            leftover_component = [comp for comp in components if comp not in factored_components]
            lumped_component = [{var for comp in leftover_component for var in comp}]
            components = factored_components + lumped_component
            components = [comp for comp in components if len(comp)>0]

        # print("factored_components: " + str(factored_components))
        # print("lumped_component: " + str(lumped_component))
        # The idea is to express this term as ceoff * np.prod([term_moments])
        term_moments = []
        for comp in components:
            # Construct the variable power mapping for this component.
            comp_vpm = {var : term_vpm[var] for var in comp}
            
            # Find a moment for this component in moments. If one doesn't exist,
            # create a new one.
            all_moments = moments + new_moments
            equivalent_moments = [m for m in all_moments if m.same_vpm(comp_vpm)]

            if len(equivalent_moments)==0:
                moment = Moment(comp_vpm)
                new_moments.append(moment)
            elif len(equivalent_moments)==1:
                moment = equivalent_moments[0]
            else:
                raise Exception("Found two instances of Moment in the set 'moments' that match comp_vpm.\
                                 This is an issue because the elements in 'moments' should be unique.")
            
            term_moments.append(moment)
        terms.append(coeff * np.prod(term_moments))
    return sum(terms), new_moments