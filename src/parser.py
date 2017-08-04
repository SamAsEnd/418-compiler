from src.nodes import *


def parse_comment(tokens):
    return Comment(tokens[0])


def parse_expression(tokens):
    if len(tokens) == 1:
        try:
            return Number(int(tokens[0]))
        except ValueError:
            return Variable(tokens[0])
    elif tokens[1] == '+':
        return Addition(parse_expression(tokens[0:1]), parse_expression(tokens[2:3]))
    elif tokens[1] == '-':
        return Subtraction(parse_expression(tokens[0:1]), parse_expression(tokens[2:3]))
    elif tokens[1] == '*':
        return Multiplication(parse_expression(tokens[0:1]), parse_expression(tokens[2:3]))
    elif tokens[1] == '/':
        return Division(parse_expression(tokens[0:1]), parse_expression(tokens[2:3]))
    elif tokens[1] == '%':
        return Modulus(parse_expression(tokens[0:1]), parse_expression(tokens[2:3]))


def parse_var_declare(tokens):
    if len(tokens) == 1:
        exp = Number(0)
    else:
        exp = parse_expression(tokens[1:])

    return VarDeclare(Variable(tokens[0]), exp)


def parse_assignment(tokens):
    exp = parse_expression(tokens[1:])

    return Assignment(Variable(tokens[0]), exp)


def parse_condition(tokens):
    first_op = parse_expression(tokens[0])
    second_op = parse_expression(tokens[2])

    if tokens[1] == '>':
        return GreaterThan(first_op, second_op)
    elif tokens[1] == '>=':
        return GreaterOrEqualTo(first_op, second_op)
    elif tokens[1] == '<':
        return LessThan(first_op, second_op)
    elif tokens[1] == '<=':
        return LessOrEqualTo(first_op, second_op)
    else:
        return EqualTo(first_op, second_op)

def parse_rest(tokens_group):
    # TODO: here
    buffer = []
    nest = 0

    counter = 1
    while counter < len(tokens_group):
        tokens = tokens_group[counter]
        if tokens[0] in ['elif', 'else', 'end'] and nest == 0:
            true = parse(buffer)
            if tokens[0] == 'end':
                return Conditional(condition, true, CompoundStatement())
            elif tokens[0] == 'end':
                return parse_till_other_option(tokens_group)
            else tokens[0] == 'else':
                return parse_till_other_option(tokens_group)
        else:
            buffer.append(tokens)

    false = CompoundStatement()

def parse_options(tokens_group):
    condition = parse_condition(tokens_group[0][1:4])



def parse_while(tokens):
    true = CompoundStatement()
    false = CompoundStatement()


def parse_write(tokens):
    pass


def parse_read(tokens):
    pass


parsers = {
    'comment': parse_comment,
    'var declare': parse_var_declare,
    'assignment': parse_assignment,
    'while': parse_while,
    'write': parse_write,
    'read': parse_read,
}


def parse(tokens):
    statements = CompoundStatement()
    buffer = []

    for name, token in tokens:
        if name not in ['if', 'elif', 'else', 'while']:
            statements.add(parsers[name](token))
        elif name == 'end':
            if buffer[0][0] == 'if':
                buffer.append((name, token))
                parse_options(buffer)
            else:
                parse_while(buffer)
            buffer.clear()
        else:
            buffer.append((name, token))

    return statements
