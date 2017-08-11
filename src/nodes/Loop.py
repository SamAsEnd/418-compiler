from nodes.CompoundStatement import CompoundStatement
from nodes.Condition import Condition
from nodes.Statement import Statement


class Loop(Statement):
    def __init__(self, condition: Condition, true: CompoundStatement):
        self.condition = condition
        self.true = true

    def __str__(self):
        return """
            while %s do
                %s
            end
            """ % (self.condition, self.true)
