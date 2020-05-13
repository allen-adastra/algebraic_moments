import sympy as sp
import networkx as nx

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
            string += str(var) + str(power) + "_"
        # Remove the underscore at the end.
        string = string.strip("_")
        return string