from nodes.Statement import Statement
from nodes.Value import Value


class WriteValue(Statement):
    def __init__(self, variable: Value):
        self.variable = variable

    def __str__(self):
        return 'write ' + str(self.variable)
