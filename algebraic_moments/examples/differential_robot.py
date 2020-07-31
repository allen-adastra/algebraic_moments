import algebraic_moments.objects as ao
from algebraic_moments.tree_ring import tree_ring
import sympy as sp

def differential_robot():
    # Declare the state variables.
    x = ao.StateVariable("x")
    y = ao.StateVariable("y")
    c = ao.StateVariable("c")
    s = ao.StateVariable("s")
    state_dependencies = [(x, y), (x, c), (x, s), (y, c), (y, s)]

    # Declare the disturbance vector.
    sol = ao.RandomVariable("sol") # sin((dt/d) * omega_l)
    sor = ao.RandomVariable("sor") # sin((dt/d) * omega_r)
    col = ao.RandomVariable("col") # cos((dt/d) * omega_l)
    cor = ao.RandomVariable("cor") # cos((dt/d) * omega_r)
    omegals = ao.RandomVariable("omegals") # omegals = (dt/2)*omega_l
    omegars = ao.RandomVariable("omegars") # omegars = (dt/2)*omega_r
    disturbance_dependencies = [(sol, col), (sor, cor), (sol, omegals), (col, omegals), (sor, omegars), (cor, omegars)]
    disturbance_vector = ao.RandomVector([sol, col, sor, cor, omegals, omegars], disturbance_dependencies)

    # Declare the control variables.
    sv = ao.DeterministicVariable("sv") # sv = sin((dt/d) * (v_r - v_l))
    cv = ao.DeterministicVariable("cv") # cv = cos((dt/d) * (v_r - v_l))
    vls = ao.DeterministicVariable("vls") # vls = (dt/2)*vl
    vrs = ao.DeterministicVariable("vrs") # vrs = (dt/2)*vr
    control_variables = [sv, cv, vls, vrs]

    # OPTIONAL: code to derive the trig expansions
    # theta = ao.StateVariable("theta")
    # v = ao.StateVariable("v")
    # print(sp.expand_trig(sp.cos(theta  + v + omegars - omegals)))
    # print(sp.expand_trig(sp.sin(theta + v + omegars - omegals)))
    
    # Instantiate the PolyDynamicalSystem
    state_dynamics = {
        x : x + (vls + vrs + omegals + omegars) * c,
        y : y + (vls + vrs + omegals + omegars) * s,
        c : ((-s*sv + c*cv)*sor + (s*cv + sv*c)*cor)*sol + ((-s*sv + c*cv)*cor - (s*cv + sv*c)*sor)*col,
        s : ((-s*sv + c*cv)*sor + (s*cv + sv*c)*cor)*col - ((-s*sv + c*cv)*cor - (s*cv + sv*c)*sor)*sol
    }
    pds = ao.PolyDynamicalSystem(state_dynamics, control_variables, disturbance_vector, state_dependencies)

    # Declare the initial moment state.
    Ex = ao.Moment({x : 1})
    Ey = ao.Moment({y : 1})
    Ex2 = ao.Moment({x : 2})
    Ey2 = ao.Moment({y : 2})
    Exy = ao.Moment({x:1, y:1})
    initial_moment_state = [Ex, Ey, Ex2, Ey2, Exy]

    # Run tree_ring to arrive at a MomentStateDynamicalSystem.
    msds = tree_ring(initial_moment_state, pds, reduced=True)

    msds.print_cpp()
    msds.print_cpp_python_structures()

differential_robot()