import sys

from compilers.Compiler import Compiler
from nodes import *


class PythonInterpreter(Compiler):
    def __init__(self, tree: CompoundStatement) -> None:
        super().__init__(tree)
        self.tree = tree
        self.code = "# 418: I'm a Teapot and interpreter but not a compiler"
        self.vars = {}

    def compile(self):
        pass

    def build(self, args):
        if args.execute:
            self.execute(self.tree)

    def execute(self, stmt: Statement):
        if isinstance(stmt, VarDeclare) or isinstance(stmt, Assignment):
            self.vars[stmt.variable.name] = self.value(stmt.expression)
        elif isinstance(stmt, Read):
            self.vars[stmt.variable.name] = input()
        elif isinstance(stmt, WriteValue):
            sys.stdout.write(str(self.value(stmt.variable)))
        elif isinstance(stmt, WriteString):
            sys.stdout.write(stmt.string.string.replace('"', '').replace('\\n', '\n'))
        elif isinstance(stmt, Comment):
            pass
        elif isinstance(stmt, Loop):
            while self.condition(stmt.condition):
                self.execute(stmt.true)
        elif isinstance(stmt, Conditional):
            if self.condition(stmt.condition):
                self.execute(stmt.true)
            else:
                self.execute(stmt.false)
        elif isinstance(stmt, CompoundStatement):
            for s in stmt:
                self.execute(s)
        else:
            raise NotImplementedError(str(stmt.__class__) + ' not implemented')

    def value(self, expression: Expression):
        if isinstance(expression, Number):
            return expression.number
        elif isinstance(expression, Variable):
            return int(self.vars[expression.name])
        elif isinstance(expression, Addition):
            return self.value(expression.first_operand) + self.value(expression.second_operand)
        elif isinstance(expression, Subtraction):
            return self.value(expression.first_operand) - self.value(expression.second_operand)
        elif isinstance(expression, Multiplication):
            return self.value(expression.first_operand) * self.value(expression.second_operand)
        elif isinstance(expression, Division):
            return self.value(expression.first_operand) // self.value(expression.second_operand)
        elif isinstance(expression, Modulus):
            return self.value(expression.first_operand) % self.value(expression.second_operand)
        else:
            raise NotImplementedError(str(expression.__class__) + ' not implemented')

    def condition(self, condition: Condition):
        if isinstance(condition, EqualTo):
            return self.value(condition.first_operand) == self.value(condition.second_operand)
        elif isinstance(condition, NotEqualTo):
            return self.value(condition.first_operand) != self.value(condition.second_operand)
        elif isinstance(condition, GreaterThan):
            return self.value(condition.first_operand) > self.value(condition.second_operand)
        elif isinstance(condition, GreaterOrEqualTo):
            return self.value(condition.first_operand) >= self.value(condition.second_operand)
        elif isinstance(condition, LessThan):
            return self.value(condition.first_operand) < self.value(condition.second_operand)
        elif isinstance(condition, LessOrEqualTo):
            return self.value(condition.first_operand) <= self.value(condition.second_operand)
        else:
            raise NotImplementedError(str(condition.__class__) + ' not implemented')
