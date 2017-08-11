from nodes.Value import Value


class Condition:
    def __init__(self, first_operand: Value, second_operand: Value):
        self.first_operand = first_operand
        self.second_operand = second_operand
