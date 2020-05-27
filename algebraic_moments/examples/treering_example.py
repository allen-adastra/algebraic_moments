import algebraic_moments.objects as ao
from algebraic_moments.tree_ring import tree_ring

def treering_example():
    # Declare the state variables.
    x = ao.StateVariable("x")
    y = ao.StateVariable("y")
    v = ao.StateVariable("v")
    c = ao.StateVariable("c")
    s = ao.StateVariable("s")
    state_dependencies = [(x, y), (x, v), (x, c), (x, s), (y, v), (y, c), (y, s)]

    # Declare the disturbance vector.
    cw = ao.RandomVariable("cw")
    sw = ao.RandomVariable("sw")
    wv = ao.RandomVariable("wv")
    disturbance_dependencies = [(cw, sw)]
    disturbance_vector = ao.RandomVector([cw, sw, wv], disturbance_dependencies)

    # Declare the control variables.
    control_variables = []

    # Declare the state dynamics.
    state_dynamics = {
        x : x + v * c,
        y : y + v * s,
        v : v + wv,
        c : c * cw - s * sw,
        s : s * cw + c * sw
    }

    # Instantiate the PolyDynamicalSystem
    pds = ao.PolyDynamicalSystem(state_dynamics, control_variables, disturbance_vector, state_dependencies)

    # Declare the initial moment state.
    Ex = ao.Moment("Ex", {x : 1})
    Ey = ao.Moment("Ey", {y : 1})
    Ex2 = ao.Moment("Ex2", {x : 2})
    Ey2 = ao.Moment("Ey2", {y : 2})
    Exy = ao.Moment("Ex_Ey", {x:1, y:1})
    initial_moment_state = [Ex, Ey, Ex2, Ey2, Exy]

    # Run tree_ring.
    tree_ring(initial_moment_state, pds)

    for m in initial_moment_state:
        print(m)

treering_example()