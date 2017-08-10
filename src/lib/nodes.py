from abc import ABC
from collections import Iterable


class Expression(ABC):
    pass


class Value(Expression):
    pass


class Number(Value):
    def __init__(self, number: int):
        if abs(number) > 2 ** 31:
            raise SyntaxError(str(number) + ' number is out of range')
        self.number = number

    def __str__(self):
        return str(self.number)


class String:
    def __init__(self, string: str):
        self.string = string

    def __str__(self):
        return self.string


class Variable(Value):
    KEYWORDS = 'var if elif else while do end read write writeln'.split()

    def __init__(self, name: str):
        if name in self.KEYWORDS:
            raise SyntaxError('Error: ' + name + ' is a keyword')
        self.name = name

    def __str__(self):
        return self.name


class ArithmeticExpression(Expression):
    def __init__(self, first_operand: Value, second_operand: Value):
        self.first_operand = first_operand
        self.second_operand = second_operand


class Addition(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' + ' + str(self.second_operand)


class Subtraction(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' - ' + str(self.second_operand)


class Multiplication(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' * ' + str(self.second_operand)


class Division(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' / ' + str(self.second_operand)


class Modulus(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' % ' + str(self.second_operand)


class Condition:
    def __init__(self, first_operand: Value, second_operand: Value):
        self.first_operand = first_operand
        self.second_operand = second_operand


class GreaterThan(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' > ' + str(self.second_operand)


class LessThan(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' < ' + str(self.second_operand)


class GreaterOrEqualTo(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' >= ' + str(self.second_operand)


class LessOrEqualTo(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' <= ' + str(self.second_operand)


class EqualTo(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' ~ ' + str(self.second_operand)


class NotEqualTo(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(self, first_operand, second_operand)

    def __str__(self):
        return str(self.first_operand) + ' !~ ' + str(self.second_operand)


class Comment:
    def __init__(self, string: str):
        self.string = string

    def __str__(self):
        return '# ' + self.string


class Statement:
    pass


class VarDeclare(Statement):
    def __init__(self, variable: Variable, expression: Value):
        self.variable = variable
        self.expression = expression

    def __str__(self):
        return 'var ' + str(self.variable) + ' = ' + str(self.expression)


class Assignment(Statement):
    def __init__(self, variable: Variable, expression: Expression):
        self.variable = variable
        self.expression = expression

    def __str__(self):
        return str(self.variable) + ' = ' + str(self.expression)


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


class Conditional(Statement):
    def __init__(self, condition: Condition, true: CompoundStatement, false: CompoundStatement):
        self.condition = condition
        self.true = true
        self.false = false

    def __str__(self):
        return 'if ' + str(self.condition) + ' do \n' + \
               str(self.true) + '\n' + \
               'else do \n' + \
               str(self.false) + '\n' + \
               'end\n'


class Loop(Statement):
    def __init__(self, condition: Condition, true: CompoundStatement):
        self.condition = condition
        self.true = true

    def __str__(self):
        return 'while ' + str(self.condition) + ' do \n' + \
               str(self.true) + '\n' + \
               'end\n'


class Read(Statement):
    def __init__(self, variable: Variable):
        self.variable = variable

    def __str__(self):
        return 'read ' + str(self.variable)


class WriteString(Statement):
    def __init__(self, string: String):
        self.string = string

    def __str__(self):
        return 'write ' + str(self.string)


class WriteValue(Statement):
    def __init__(self, variable: Value):
        self.variable = variable

    def __str__(self):
        return 'write ' + str(self.variable)
