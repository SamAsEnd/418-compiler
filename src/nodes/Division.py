from nodes.ArithmeticExpression import ArithmeticExpression
from nodes.Value import Value


class Division(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' / ' + str(self.second_operand)
