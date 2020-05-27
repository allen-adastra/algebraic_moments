import numpy as np
import sympy as sp
from algebraic_moments.moment_expressions import moment_expression
from copy import deepcopy

def tree_ring(initial_moment_state, poly_dynamical_system):
    """[summary]
    """
    for moment in initial_moment_state:
        expand(moment, initial_moment_state, poly_dynamical_system)

def expand(moment, moment_state, poly_dynamical_system):
    moment_dynamics = np.prod([poly_dynamical_system.dynamics[var] for var, power in moment.vpm.items()\
                               if var in poly_dynamical_system.state_variables])

    # system_random_vector is a random vector composed of all state, control, and disturbance variables.
    system_random_vector = poly_dynamical_system.system_random_vector

    expression, new_moments = moment_expression(moment_dynamics, system_random_vector, moment_state)

    # Filter down to state moments.
    new_state_moments = [m for m in new_moments if set(m.variables).issubset(poly_dynamical_system.state_variables)]
    new_disturbance_moments = [m for m in new_moments if m not in new_state_moments] # TODO: use this..

    moment_state += new_state_moments

    for new_m in new_state_moments:
        expand(new_m, moment_state, poly_dynamical_system)