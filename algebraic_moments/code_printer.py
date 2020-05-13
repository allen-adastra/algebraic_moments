from sympy.printing import octave_code
from sympy.printing.pycode import pycode

class CodePrinter(object):
    def print_moment_constraints(self, moment_constraints, moments, language):
        # Essentially a switch statement.
        method = getattr(self, language, lambda: "Input language is not supported.")
        return method(moment_constraints, moments)

    def python(self, moment_constraints, moments):
        for moment in moments:
            print(str(moment) + " = input_moments[\"" + str(moment) + "\"]")

        for i, cons in enumerate(moment_constraints):
            print("g" + str(i) + " = " + pycode(cons))

    def matlab(self, moment_constraints, moments):
        """The octave function should produce code that is compatible with matlab.
        """
        return self.octave(moment_constraints, moments)

    def octave(self, moment_constraints, moments):
        for moment in moments:
            print(str(moment) + " = input_moments." + str(moment) + ";")

        for i, cons in enumerate(moment_constraints):
            print(octave_code(cons, assign_to="g"+str(i)))