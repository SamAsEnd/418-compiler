from nodes.Condition import Condition
from nodes.Value import Value


class GreaterThan(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' > ' + str(self.second_operand)
