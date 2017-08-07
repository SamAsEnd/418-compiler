from lib.nodes import *


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
    first_op = parse_expression([tokens[0]])
    second_op = parse_expression([tokens[2]])

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


def parse_the_rest(tokens_group, split_at):
    split_at.append('end')

    nest = 0
    counter = 0

    while counter < len(tokens_group):
        tokens = tokens_group[counter]

        if nest == 0 and tokens[0] in split_at:
            true = parse(tokens_group[:counter])
            if tokens[0] == 'end':
                return true, CompoundStatement()
            elif tokens[0] == 'elif':
                return true, parse_options(tokens_group[counter:])
            else:
                return true, parse(tokens_group[counter + 1:len(tokens_group) - 1])

        if tokens[0] in ['if', 'while']:
            nest += 1
        elif tokens[0] == 'end' and nest > 0:
            nest -= 1

        counter += 1


def parse_options(tokens_group):
    condition = parse_condition(tokens_group[0][1])
    true, rest = parse_the_rest(tokens_group[1:], ['elif', 'else'])

    return Conditional(condition, true, rest)


def parse_while(tokens_group):
    condition = parse_condition(tokens_group[0][1])
    true, rest = parse_the_rest(tokens_group[1:], [])

    return Loop(condition, true)


def parse_write(tokens):
    if tokens[0].startswith('"'):
        return WriteString(String(tokens[0]))
    else:
        return WriteValue(parse_expression(tokens))


def parse_read(tokens):
    return Read(Variable(tokens[0]))


SIMPLE_PARSERS = {
    'comment': parse_comment,
    'var declare': parse_var_declare,
    'assignment': parse_assignment,
    'write': parse_write,
    'read': parse_read,
}


def parse(tokens):
    statements = CompoundStatement()

    buffer = []
    nested = 0
    counter = 0

    while counter < len(tokens):
        name, token = tokens[counter]
        if len(buffer) == 0 and name in SIMPLE_PARSERS.keys():
            statements.add(SIMPLE_PARSERS[name](token))
        else:
            buffer.append(tokens[counter])

            if name in ['if', 'while']:
                nested += 1
            elif name == 'end':
                if nested == 1:
                    if buffer[0][0] == 'if':
                        statements.add(parse_options(buffer))
                    elif buffer[0][0] == 'while':
                        statements.add(parse_while(buffer))
                    buffer.clear()
                    nested = 0
                else:
                    nested -= 1

        counter += 1

    if len(buffer) != 0:
        sys.stderr.write('Error: You forgot to and "end" somewhere')
        exit(1)

    return statements
