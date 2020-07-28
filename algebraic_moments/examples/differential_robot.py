import algebraic_moments.objects as ao
from algebraic_moments.tree_ring import tree_ring
import sympy as sp

def differential_robot():
    x = ao.StateVariable("x")
    y = ao.StateVariable("y")
    c = ao.StateVariable("c")
    s = ao.StateVariable("s")
    state_dependencies = [(x, y), (x, c), (x, s), (y, c), (y, s)]

    # Declare the disturbance vector.
    # sol : sin((dt/d) * omega_l)
    # sor : sin((dt/d) * omega_r)
    # col : cos((dt/d) * omega_l)
    # cor : cos((dt/d) * omega_r)
    sol = ao.RandomVariable("sol")
    sor = ao.RandomVariable("sor")
    col = ao.RandomVariable("col")
    cor = ao.RandomVariable("cor")
    omegals = ao.RandomVariable("omegals") # omegals = (dt/2)*omega_l
    omegars = ao.RandomVariable("omegars") # omegars = (dt/2)*omega_r
    disturbance_dependencies = [(sol, col), (sor, cor), (sol, omegals), (col, omegals), (sor, omegars), (cor, omegars)]
    disturbance_vector = ao.RandomVector([sol, col, sor, cor, omegals, omegars], disturbance_dependencies)

    # Declare the control variables.
    svl = ao.DeterministicVariable("svl") # svl = sin((dt/d) * v_l)
    svr = ao.DeterministicVariable("svr") # svr = sin((dt/d) * v_r)
    cvl = ao.DeterministicVariable("cvl") # cvl = cos((dt/d) * v_l)
    cvr = ao.DeterministicVariable("cvr") # cvr = cos((dt/d) * v_r)
    vls = ao.DeterministicVariable("vls") # vls = (dt/2)*vl
    vrs = ao.DeterministicVariable("vrs") # vrs = (dt/2)*vr
    dt_over_two = ao.DeterministicVariable("dt_over_two") # dt/2
    dt_over_d = ao.DeterministicVariable("dt_over_d") # dt/d
    control_variables = [svl, svr, cvl, cvr, vls, vrs, dt_over_two, dt_over_d]

    # Code to derive the trig expansions
    # theta = ao.StateVariable("theta")
    # print(sp.expand_trig(sp.cos(theta - vls - omegals + vrs + omegars)))
    # print(sp.expand_trig(sp.sin(theta - vls - omegals + vrs + omegars)))
    

    state_dynamics = {
        x : x + dt_over_two * (vls + vrs + omegals + omegars) * c,
        y : y + dt_over_two * (vls + vrs + omegals + omegars) * s,
        c : (((-sor*s + cor*c)*svr + (sor*c + s*cor)*cvr)*sol + ((-sor*s + cor*c)*cvr - (sor*c + s*cor)*svr)*col)*cvl + (((-sor*s + cor*c)*svr + (sor*c + s*cor)*cvr)*col - ((-sor*s + cor*c)*cvr - (sor*c + s*cor)*svr)*sol)*svl,
        s : -(((-sor*s + cor*c)*svr + (sor*c + s*cor)*cvr)*sol + ((-sor*s + cor*c)*cvr - (sor*c + s*cor)*svr)*col)*svl + (((-sor*s + cor*c)*svr + (sor*c + s*cor)*cvr)*col - ((-sor*s + cor*c)*cvr - (sor*c + s*cor)*svr)*sol)*cvl
    }
    
    # Instantiate the PolyDynamicalSystem
    pds = ao.PolyDynamicalSystem(state_dynamics, control_variables, disturbance_vector, state_dependencies)

    # Declare the initial moment state.
    Ex = ao.Moment({x : 1})
    Ey = ao.Moment({y : 1})
    Ex2 = ao.Moment({x : 2})
    Ey2 = ao.Moment({y : 2})
    Exy = ao.Moment({x:1, y:1})
    initial_moment_state = [Ex, Ey, Ex2, Ey2, Exy]

    # Run tree_ring to arrive at a MomentStateDynamicalSystem.
    msds = tree_ring(initial_moment_state, pds, reduced=False)

    msds.print_python()

differential_robot()