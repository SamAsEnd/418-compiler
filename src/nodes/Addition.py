from nodes.Value import Value
from nodes.ArithmeticExpression import ArithmeticExpression


class Addition(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' + ' + str(self.second_operand)
