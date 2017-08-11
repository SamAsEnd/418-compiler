from collections import Iterable

from nodes.Statement import Statement


class CompoundStatement(Statement, Iterable):
    def __init__(self):
        self.statements = []

    def add(self, other: Statement):
        self.statements.append(other)

    def __iter__(self):
        for statement in self.statements:
            yield statement

    def __str__(self):
        return '\n'.join([str(stmt) for stmt in self])
