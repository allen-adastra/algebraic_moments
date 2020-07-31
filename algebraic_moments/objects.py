import sympy as sp
from sympy.printing import octave_code
from sympy.printing.pycode import pycode
from sympy.printing.ccode import ccode
import networkx as nx
from enum import Enum

class ConcentrationInequalityType(Enum):
    CANTELLI = 0
    VP = 1
    GAUSS = 2

class ConcentrationInequality(object):
    def __init__(self, moment_expressions, inequality_type):
        self._moment_expressions = moment_expressions
        self._type = inequality_type

    def build_expressions(self):
        first_moment = sp.Symbol("first_moment")
        variance = sp.Symbol("variance")

        if self._type == ConcentrationInequalityType.CANTELLI:
            bound_expr = variance/(variance + first_moment**2)
            condition_expr = -first_moment

        elif self._type == ConcentrationInequalityType.VP:
            bound_expr = (4.0/9.0) * variance/(variance + first_moment**2)
            condition_expr = -first_moment + (5.0*variance/3.0)**0.5

        elif self._type == ConcentrationInequalityType.GAUSS:
            bound_expr = (2.0/9.0) * (variance/first_moment**2)
            condition_expr = -first_moment + (2.0/3.0) * (variance)**0.5
        else:
            raise Exception("Invalid type in ConcentrationInequality.")
            
        return bound_expr, condition_expr

    def print_python(self):
        bound_expr, condition_expr = self.build_expressions()
        self._moment_expressions.print_python()
        print("\n# Establish the probability bound.")
        print("# We need necessary_condition<=0 for this bound to hold.")
        print("variance = second_moment - first_moment**2")
        print("probability_bound = " + str(bound_expr))
        print("necessary_condition = " + str(condition_expr))
    
    def print_matlab(self):
        return self.print_octave()

    def print_octave(self):
        bound_expr, condition_expr = self.build_expressions()
        self._moment_expressions.print_octave()
        print("\n% Establish the probability bound.")
        print("% We need necessary_condition<=0 for this bound to hold.")
        print("variance = second_moment - first_moment.^2;")
        print(octave_code(bound_expr, assign_to="probability_bound"))
        print(octave_code(condition_expr, assign_to="necessary_condition"))


class MomentExpressions(object):
    def __init__(self, moment_expressions, moments, random_vector, deterministic_variables):
        self._moment_expressions = moment_expressions
        self._moments = moments
        self._random_vector = random_vector
        self._deterministic_variables = deterministic_variables

    @property
    def moment_expressions(self):
        return self._moment_expressions

    def print_python(self, multi_idx_keys = False):
        """Print python code.

        Args:
            multi_idx_keys (bool, optional): If true, input_moments keys are multi-indices. Defaults to False.
        """
        # Parse required inputs.
        print("# Parse required inputs.")
        for moment in self._moments:
            if multi_idx_keys:
                # Get the multi index of the moment relative to self._random_vector.
                dict_input = str(self._random_vector.multi_idx(moment.vpm))
            else:
                dict_input = "\"" + str(moment) + "\""

            print(str(moment) + " = input_moments[" + dict_input + "]")

        for det_var in self._deterministic_variables:
            print(str(det_var) +" = input_deterministic[\"" + str(det_var) + "\"]" )

        # Generate constraint expressions.
        print("\n# Moment expressions.")
        for name, cons in self._moment_expressions.items():
            print(str(name) + " = " + pycode(cons))

    def print_matlab(self):
        """The sympy function octave_code is designed to produce MATLAB compatible code.
        """
        return self.print_octave()

    def print_octave(self):
        # Parse required inputs.
        print("% Parse required inputs.")
        for moment in self._moments:
            print(str(moment) + " = input_moments." + str(moment) + ";")
            
        for det_var in self._deterministic_variables:
            print(str(det_var) + " = input_deterministic." + str(det_var) + ";")

        # Generate constraint expressions
        print("\n% Moment expressions.")
        for name, cons in self._moment_expressions.items():
            print(octave_code(cons, assign_to=str(name)))

class MomentStateDynamicalSystem(object):
    def __init__(self, moment_state_dynamics, disturbance_moments, control_variables):
        """

        Args:
            moment_state_dynamics (dict Moment -> SymPy expression):
        """
        self._moment_state = list(moment_state_dynamics.keys())
        self._moment_state_dynamics = moment_state_dynamics
        self._disturbance_moments = disturbance_moments
        self._control_variables = control_variables

    def print_cpp(self):
        # Print imports necessary.
        print("#include <cmath> \nusing namespace std;\n")

        # Generate code for input structures.
        moment_state_struct = "struct MomentState {\n"
        for m, _ in self._moment_state_dynamics.items():
            moment_state_struct += "double " + str(m) + ";\n"
        moment_state_struct += "};\n"
        print(moment_state_struct)

        disturbance_moment_struct = "struct DisturbanceMoments{\n"
        for dist_moment in self._disturbance_moments:
            disturbance_moment_struct += "double " + str(dist_moment) + ";\n"
        disturbance_moment_struct += "};\n"
        print(disturbance_moment_struct)

        controls_struct = "struct Controls{\n"
        for control_var in self._control_variables:
            controls_struct += "double " + str(control_var) + ";\n"
        controls_struct += "};\n"
        print(controls_struct)

        # Generate code for the function.
        print("void PropagateMoments(const MomentState *prev_moment_state, const DisturbanceMoments *disturbance_moments, const Controls *control_inputs, MomentState *moment_state){")

        print("// Aliases for the required inputs.")
        for m, dynamics in self._moment_state_dynamics.items():
            print("const double &" + str(m) + " = prev_moment_state->" + str(m) + ";")
        print("\n")
        for dist_moment in self._disturbance_moments:
            print("const double &" + str(dist_moment) + " = disturbance_moments->" + str(dist_moment) + ";")
        if self._control_variables:
            print("\n")
            for control_var in self._control_variables:
                print("const double &" + str(control_var) + " = control_inputs->" + str(control_var) + ";")
        print("\n// Dynamics updates.")
        for m, dynamics in self._moment_state_dynamics.items():
            print("moment_state->" + str(m) + " = " + str(ccode(dynamics)) + ";\n")
        print("return; \n }")
    
    def print_cpp_python_structures(self):
        # Generate code for Python bindings to input structures vis ctypes.
        def structure_python_binding_generator(structure_name, variable_names):
            # Generator that assumes all fields are c_double.

            struct = "class " + str(structure_name) + "(ctypes.Structure):\n"
            struct += "    _fields_ = ["
            for var in variable_names:
                struct += "(\"" + str(var)+ "\", c_double),"
            # Strip the final comma
            struct = struct[:-1]
            struct+="]"
            return struct
        moment_state_struct = structure_python_binding_generator("MomentState", [m for m, _ in self._moment_state_dynamics.items()])
        disturbance_moment_struct = structure_python_binding_generator("DisturbanceMoments", self._disturbance_moments)
        control_struct = structure_python_binding_generator("Controls", self._control_variables)
        print(moment_state_struct)
        print(disturbance_moment_struct)
        print(control_struct)

    def print_python(self):
        print("# Parse required inputs.")
        for m, dynamics in self._moment_state_dynamics.items():
            print(str(m) + " = prev_moment_state[\"" + str(m) + "\"]")
        print("\n")
        for dist_moment in self._disturbance_moments        :
            print(str(dist_moment) + " = disturbance_moments[\"" + str(dist_moment) + "\"]")
        if self._control_variables:
            print("\n")
            for control_var in self._control_variables:
                print(str(control_var) + " = control_inputs[\"" + str(control_var) + "\"]")
        print("\n#Dynamics updates.")
        print("moment_state = dict()")
        for m, dynamics in self._moment_state_dynamics.items():
            print("moment_state[\"" + str(m) + "\"] = " + str(dynamics))

    def print_matlab(self):
        return self.print_octave()

    def print_octave(self):
        print("% Parse required inputs.")
        for m, dynamics in self._moment_state_dynamics.items():
            print(str(m) + " = prev_moment_state." + str(m) + ";")
        print("\n")
        for dist_moment in self._disturbance_moments        :
            print(str(dist_moment) + " = disturbance_moments." + str(dist_moment) + ";")
        if self._control_variables:
            print("\n")
            for control_var in self._control_variables:
                print(str(control_var) + " = control_inputs." + str(control_var) + ";")
        print("\n%Dynamics updates.")
        for m, dynamics in self._moment_state_dynamics.items():
            print("moment_state." + str(m) + " = " + str(dynamics) + ";")

class DeterministicVariable(sp.Symbol):
    def __init__(self, string_rep):
        assert " " not in string_rep, "Spaces not allowed in the string representation of DeterministicVariable"
        sp.Symbol.__init__(string_rep)

"""
"""
class RandomVariable(sp.Symbol):
    def __init__(self, string_rep):
        assert " " not in string_rep, "Spaces not allowed in the string representation of RandomVariable"
        sp.Symbol.__init__(string_rep)

class StateVariable(RandomVariable):
    pass

class PolyDynamicalSystem(object):
    def __init__(self, state_dynamics, control_variables, disturbance_vector, state_dependencies):
        """ A discrete time polynomial stochastic system.

        Args:
            state_dynamics (dict StateVariable -> SymPy Expression): dynamics of the state variables.
            control_variables (list of DeterministicVariable): control variables of the system.
            disturbance_vector (RandomVector): random vector of disturbances of the system.
            state_dependencies (list of tuples of StateVariable): pairwise dependence between instances of StateVariable.

        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """
        self._state_variables = list(state_dynamics.keys())
        self._control_variables = control_variables
        self._dynamics = state_dynamics
        self._state_dependence_graph = DependenceGraph.from_lists(self._state_variables, state_dependencies)
        self._state_random_vector = RandomVector(self._state_variables, state_dependencies)

        # Create an instance of RandomVector that encapsulates the state and disturbance variables.
        self._disturbance_vector = disturbance_vector
        self._system_random_vector = RandomVector(self._state_variables + disturbance_vector.variables,
                                                  self._state_dependence_graph.edges + disturbance_vector.dependence_graph.edges)
    
    @property
    def dynamics(self):
        """ 
        Returns:
            dict StateVariable -> SymPy expression: dictionary of dynamics.
        """
        return self._dynamics

    @property
    def state_variables(self):
        return self._state_variables
    
    @property
    def state_random_vector(self):
        return self._state_random_vector

    @property
    def system_random_vector(self):
        return self._system_random_vector

    @property
    def control_variables(self):
        return self._control_variables
    
    @property
    def disturbance_variables(self):
        return self._disturbance_vector.variables

class DependenceGraph(object):
    def __init__(self, nx_graph):
        self._nx_graph = nx_graph
    
    def subgraph_components(self, random_variables):
        """ Find the connected components of the subgraph induced by random_variables.

        Args:
            random_variables (list of RandomVariable): 

        Returns:
            list of sets of RandomVariable: [description]
        """
        subgraph = self._nx_graph.subgraph(random_variables)
        connected_components = list(nx.connected_components(subgraph))
        return connected_components

    @property
    def edges(self):
        return list(self._nx_graph.edges)

    @property
    def nx_graph(self):
        return self._nx_graph
    
    @classmethod
    def from_lists(cls, variables, variable_dependencies):
        """

        Args:
            variables ([type]): [description]
            dependencies ([type]): [description]

        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """

        # Construct the dependence_graph.
        dep_graph = nx.Graph()
        dep_graph.add_nodes_from(variables)
        if variable_dependencies:
            dep_graph.add_edges_from(variable_dependencies)
        return cls(dep_graph)

class RandomVector(object):
    def __init__(self, random_variables, variable_dependencies):
        """

        Args:
            random_variables (list of instances of RandomVariable):
            variable_dependencies (list of tuples of RandomVariable): Tuples specify pairwise dependence between random variables
        """
        self._random_variables = self.sort_variables(random_variables)
        self._dependence_graph = DependenceGraph.from_lists(random_variables, variable_dependencies)
    
    @property
    def variables(self):
        return self._random_variables

    @property
    def dependence_graph(self):
        return self._dependence_graph

    def multi_idx(self, vpm):
        return tuple(vpm[var] if var in vpm.keys() else 0 for var in self._random_variables)

    def vpm(self, multi_index):
        return {self._random_variables[i] : power for i, power in enumerate(multi_index) if power>0}

    @staticmethod
    def sort_variables(variables):
        """ Sort variables by lexographical order.
        """
        return sorted(variables, key=str)

class Moment(sp.Symbol):
    def __new__(cls, vpm):
        string_rep = Moment.generate_string_rep(vpm)
        return super(Moment, cls).__new__(cls, string_rep)

    def __init__(self, vpm):
        string_rep = Moment.generate_string_rep(vpm)
        sp.Symbol.__init__(string_rep)
        self._vpm = {var : power for var, power in vpm.items() if power>0}

    def same_vpm(self, input):
        """ Check if an input vpm or instance of Moment is the same.

        Args:
            input (dict or Moment): can be a vpm or a moment.

        Raises:
            Exception: invalid input type.

        Returns:
            bool: check if input is the same as this object.
        """
        if type(input) == Moment:
            if input.vpm == self._vpm:
                return True
            else:
                return False
        elif type(input) == dict:
            if input == self._vpm:
                return True
            else:
                return False
        else:
            raise Exception("Invalid input to Moment.same_vpm.")
    
    @property
    def variables(self):
        return list(self._vpm.keys())
        
    @property
    def vpm(self):
        return self._vpm

    def multi_idx(self, random_vector):
        """ Generate the multi index w.r.t. a given random vector.

        Args:
            random_vector ([type]): [description]

        Returns:
            [type]: [description]
        """

    @staticmethod
    def generate_string_rep(variable_power_map):
        """ Construct the string rep of this moment using the variable_power_map.
            The convention is:
                - underscore _ denotes multiplication
                - Order of moments is specified by "variable_name + Pow + int"
                - variable names are sorted according to a lexographical order.
        Args:
            variable_power_map ([type]):
        """
        # Sort the variable names according to the ordering used by RandomVector.
        variable_names = RandomVector.sort_variables(variable_power_map.keys())

        # Build the string_rep.
        string_rep = ''
        for var in variable_names:
            power = variable_power_map[var]
            assert power > 0
            string_rep += str(var) + "Pow" + str(power) + "_"
        string_rep = string_rep.strip("_") # Remove the underscore at the end.
        return string_rep