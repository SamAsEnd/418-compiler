from nodes.Assignment import Assignment


class VarDeclare(Assignment):
    def __str__(self):
        return 'var ' + super().__str__()
