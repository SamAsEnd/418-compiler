from nodes.Statement import Statement
from nodes.Variable import Variable


class Read(Statement):
    def __init__(self, variable: Variable):
        self.variable = variable

    def __str__(self):
        return 'read ' + str(self.variable)
