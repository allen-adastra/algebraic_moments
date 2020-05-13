from sympy.printing import octave_code
from sympy.printing.pycode import pycode
from sympy.utilities.codegen import codegen

class CodePrinter(object):
    def print_moment_constraints(self, moment_constraints, moments, deterministic_variables, language):
        # Essentially a switch statement.
        method = getattr(self, language, lambda: "Input language is not supported.")
        return method(moment_constraints, moments, deterministic_variables)

    def python(self, moment_constraints, moments, deterministic_variables):
        # Parse required inputs.
        print("# Parse required inputs.")
        for moment in moments:
            print(str(moment) + " = input_moments[\"" + str(moment) + "\"]")

        for det_var in deterministic_variables:
            print(str(det_var) +" = input_deterministic[\"" + str(det_var) + "\"]" )

        # Generate constraint expressions.
        print("\n# Moment constraints.")
        for i, cons in enumerate(moment_constraints):
            print("g" + str(i) + " = " + pycode(cons))

    def matlab(self, moment_constraints, moments, deterministic_variables):
        """The sympy function octave_code is designed to produce MATLAB compatible code.
        """
        return self.octave(moment_constraints, moments, deterministic_variables)

    def octave(self, moment_constraints, moments, deterministic_variables):
        # Parse required inputs.
        print("% Parse required inputs.")
        for moment in moments:
            print(str(moment) + " = input_moments." + str(moment) + ";")
            
        for det_var in deterministic_variables:
            print(str(det_var) + " = input_deterministic." + str(det_var) + ";")

        # Generate constraint expressions
        print("\n% Moment constraints.")
        for i, cons in enumerate(moment_constraints):
            print(octave_code(cons, assign_to="g"+str(i)))
