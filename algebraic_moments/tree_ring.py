import numpy as np
import sympy as sp
from algebraic_moments.moment_expressions import moment_expression
from algebraic_moments.objects import MomentStateDynamicalSystem
from copy import deepcopy



def tree_ring(initial_moment_state, poly_dynamical_system, reduced=True):
    """ tree_ring is an algorithm for finding a moment state dynamical system to propagate the moments
    specified in "initial_moment_state".

    Args:
        initial_moment_state (list of Moment): moment state we want to find the dynamics for.
        poly_dynamical_system (PolyDynamicalSystem): the polynomial dynamical system we are working with.
        reduced (bool, optional): Search for a reduced MSDS or un-reduced MSDS. Defaults to True.

    Returns:
        MomentStateDynamicalSystem: resutling moment state dynamical system.
    """
    moment_state_dynamics = dict()
    disturbance_moments = set()
    for moment in initial_moment_state:
        expand(moment, initial_moment_state, moment_state_dynamics, poly_dynamical_system, disturbance_moments, reduced=reduced)
    return MomentStateDynamicalSystem(moment_state_dynamics, disturbance_moments, poly_dynamical_system.control_variables)

def expand(moment, moment_state, moment_state_dynamics, poly_dynamical_system, disturbance_moments, reduced=True):
    """ Expand a node in the search tree. TODO: decide on a better metaphor for the tree we are working with.

    Args:
        moment (Moment): the moment we are deriving the dyanmics for.
        moment_state (list of Moment): current moment state.
        moment_state_dynamics (dict Moment-> SymPy expression): dictionary for the dynamics of the moment state.
        poly_dynamical_system (PolyDynamicalSystem): the polynomial dynamical system we are working with.
        disturbance_moments (RandomVector): disturbance moments for the system.
        reduced (bool, optional): Search for a reduced MSDS or un-reduced MSDS. Defaults to True.
    """
    moment_dynamics = np.prod([poly_dynamical_system.dynamics[var]**power for var, power in moment.vpm.items()\
                               if var in poly_dynamical_system.state_variables])

    # system_random_vector is a random vector composed of all state, control, and disturbance variables.
    system_random_vector = poly_dynamical_system.system_random_vector
    if reduced==True:
        expression, new_moments = moment_expression(moment_dynamics, system_random_vector, moment_state)
    else:
        expression, new_moments = moment_expression(moment_dynamics, system_random_vector, moment_state,\
                                                    partial_reduction=set(poly_dynamical_system.disturbance_variables))

    moment_state_dynamics[moment] = expression
    
    # Update state moments and disturbance moments.
    new_state_moments = [m for m in new_moments if set(m.variables).issubset(poly_dynamical_system.state_variables)]
    new_disturbance_moments = {m for m in new_moments if m not in new_state_moments}

    moment_state += new_state_moments
    disturbance_moments.update(new_disturbance_moments)

    for new_m in new_state_moments:
        expand(new_m, moment_state, moment_state_dynamics, poly_dynamical_system, disturbance_moments)