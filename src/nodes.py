from collections import Iterable


class Expression:
    pass


class Value(Expression):
    pass


class Number(Value):
    def __init__(self, number: int):
        self.number = number


class String:
    def __init__(self, string: str):
        self.string = string


class Variable(Value):
    KEYWORDS = 'var if elif else while do end read write'.split()

    def __init__(self, name: str):
        if name in self.KEYWORDS:
            raise Exception(name + ' is a keyword')
        self.name = name


class ArithmeticExpression(Expression):
    def __init__(self, first_operand: Value, second_operand: Value):
        self.first_operand = first_operand
        self.second_operand = second_operand


class Addition(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)


class Subtraction(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)


class Multiplication(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)


class Division(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)


class Modulus(ArithmeticExpression):
    def __init__(self, first_operand: Value, second_operand: Value):
        ArithmeticExpression.__init__(self, first_operand, second_operand)


class Condition:
    def __init__(self, first_operand: Value, second_operand: Value):
        self.first_operand = first_operand
        self.second_operand = second_operand


class GreaterThan(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(first_operand, second_operand)


class LessThan(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(first_operand, second_operand)


class GreaterOrEqualTo(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(first_operand, second_operand)


class LessOrEqualTo(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(first_operand, second_operand)


class EqualTo(Condition):
    def __init__(self, first_operand: Value, second_operand: Value):
        Condition.__init__(first_operand, second_operand)


class Comment:
    def __init__(self, string: str):
        self.string = string


class Statement:
    pass


class VarDeclare(Statement):
    def __init__(self, variable: Variable, expression: Expression):
        self.variable = variable
        self.expression = expression


class Assignment(Statement):
    def __init__(self, variable: Variable, expression: Expression):
        self.variable = variable
        self.expression = expression


class CompoundStatement(Statement, Iterable):
    def __init__(self):
        self.statements = []

    def add(self, other: Statement):
        self.statements.append(other)

    def __iter__(self):
        for statement in self.statements:
            yield statement


class Conditional(Statement):
    def __init__(self, condition: Condition, true: CompoundStatement, false: CompoundStatement):
        self.condition = condition
        self.true = true
        self.false = false


class Loop(Statement):
    def __init__(self, condition: Condition, true: CompoundStatement):
        self.condition = condition
        self.true = true


class Read(Statement):
    def __init__(self, variable: Variable):
        self.variable = variable


class WriteString(Statement):
    def __init__(self, variable: Expression):
        self.variable = variable


class WriteVariable(Statement):
    def __init__(self, string: String):
        self.string = string
