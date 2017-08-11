from nodes.Expression import Expression
from nodes.Statement import Statement
from nodes.Variable import Variable


class Assignment(Statement):
    def __init__(self, variable: Variable, expression: Expression):
        self.variable = variable
        self.expression = expression

    def __str__(self):
        return str(self.variable) + ' = ' + str(self.expression)
