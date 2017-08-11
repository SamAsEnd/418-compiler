from nodes.Statement import Statement
from nodes.String import String


class WriteString(Statement):
    def __init__(self, string: String):
        self.string = string

    def __str__(self):
        return 'write ' + str(self.string)
