import sympy as sp
from sympy.printing import octave_code
from sympy.printing.pycode import pycode
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

    def print(self, language):

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
        
        # Print the code. First print the necessary moment expresssions
        # Then print the concentration inequalities.
        self._moment_expressions.print(language)
        if language == "matlab" or language == "octave":
            ConcentrationInequality.octave_printer(bound_expr, condition_expr)
        elif language == "python":
            ConcentrationInequality.python_printer(bound_expr, condition_expr)
        else:
            raise Exception("")

    @staticmethod
    def octave_printer(bound_expr, condition_expr):
        print("\n% Establish the probability bound.")
        print("% We need necessary_condition<=0 for this bound to hold.")
        print("variance = second_moment - first_moment.^2;")
        print(octave_code(bound_expr, assign_to="probability_bound"))
        print(octave_code(condition_expr, assign_to="necessary_condition"))

    @staticmethod
    def python_printer(bound_expr, condition_expr):
        print("\n# Establish the probability bound.")
        print("# We need necessary_condition<=0 for this bound to hold.")
        print("variance = second_moment - first_moment**2")
        print("probability_bound = " + str(bound_expr))
        print("necessary_condition = " + str(condition_expr))

class MomentExpressions(object):
    def __init__(self, moment_expressions, moments, deterministic_variable):
        self._moment_expressions = moment_expressions
        self._moments = moments
        self._deterministic_variables = deterministic_variable

    @property
    def moment_expressions(self):
        return self._moment_expressions

    def print(self, language):
        # Essentially a switch statement.
        method = getattr(self, language, lambda: "Input language is not supported.")
        return method(self._moment_expressions, self._moments, self._deterministic_variables)

    @staticmethod
    def python(moment_expressions, moments, deterministic_variables):
        # Parse required inputs.
        print("# Parse required inputs.")
        for moment in moments:
            print(str(moment) + " = input_moments[\"" + str(moment) + "\"]")

        for det_var in deterministic_variables:
            print(str(det_var) +" = input_deterministic[\"" + str(det_var) + "\"]" )

        # Generate constraint expressions.
        print("\n# Moment expressions.")
        for name, cons in moment_expressions.items():
            print(str(name) + " = " + pycode(cons))

    @staticmethod
    def matlab(moment_expressions, moments, deterministic_variables):
        """The sympy function octave_code is designed to produce MATLAB compatible code.
        """
        return MomentExpressions.octave(moment_expressions, moments, deterministic_variables)

    @staticmethod
    def octave(moment_expressions, moments, deterministic_variables):
        # Parse required inputs.
        print("% Parse required inputs.")
        for moment in moments:
            print(str(moment) + " = input_moments." + str(moment) + ";")
            
        for det_var in deterministic_variables:
            print(str(det_var) + " = input_deterministic." + str(det_var) + ";")

        # Generate constraint expressions
        print("\n% Moment expressions.")
        for name, cons in moment_expressions.items():
            print(octave_code(cons, assign_to=str(name)))


class DeterministicVariable(sp.Symbol):
    def __init__(self, string_rep):
        sp.Symbol.__init__(string_rep)

"""
"""
class RandomVariable(sp.Symbol):
    def __init__(self, string_rep):
        sp.Symbol.__init__(string_rep)

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

class RandomVector(object):
    def __init__(self, random_variables, variable_dependencies):
        """

        Args:
            random_variables (list of instances of RandomVariable):
            variable_dependencies (list of tuples of RandomVariable): Tuples specify pairwise dependence between random variables
        """
        self._random_variables = random_variables

        # Construct the dependence_graph.
        dep_graph = nx.Graph()
        dep_graph.add_nodes_from(self._random_variables)
        dep_graph.add_edges_from(variable_dependencies)
        self._dependence_graph = DependenceGraph(dep_graph)
    
    @property
    def variables(self):
        return self._random_variables

    @property
    def dependence_graph(self):
        return self._dependence_graph

    def vpm(self, multi_index):
        return {self._random_variables[i] : power for i, power in enumerate(multi_index) if power>0}

class Moment(sp.Symbol):
    def __new__(cls, string_rep, vpm):
        return super(Moment, cls).__new__(cls, string_rep)

    def __init__(self, string_rep, vpm):
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
    def vpm(self):
        return self._vpm

    @classmethod
    def from_vpm(cls, variable_power_map):
        string_rep = Moment.generate_string_rep(variable_power_map)
        return cls(string_rep, variable_power_map)

    @staticmethod
    def generate_string_rep(variable_power_map):
        """ Construct the string rep of this moment using the variable_power_map.

        Args:
            variable_power_map ([type]):
        """
        string = ''
        for var, power in variable_power_map.items():
            assert power > 0
            string += str(var) + "Pow" + str(power) + "_"
        # Remove the underscore at the end.
        string = string.strip("_")
        return string