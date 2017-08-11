from nodes.CompoundStatement import CompoundStatement
from nodes.Condition import Condition
from nodes.Statement import Statement


class Conditional(Statement):
    def __init__(self, condition: Condition, true: CompoundStatement, false: CompoundStatement):
        self.condition = condition
        self.true = true
        self.false = false

    def __str__(self):
        return """
            if %s do
                %s
            else do
                %s
            end
            """ % (self.condition, self.true, self.false)
