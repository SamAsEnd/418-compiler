from lib.nodes import *


def generate_c(stmt: Statement):
    code = ''
    if isinstance(stmt, VarDeclare):
        code += 'int '
        code += str(stmt.variable)
        code += ' = '
        code += str(stmt.expression)
        code += ';'
    elif isinstance(stmt, Assignment):
        code += str(stmt.variable)
        code += ' = '
        code += str(stmt.expression)
        code += ';'
    elif isinstance(stmt, Read):
        code += 'scanf("%d", &'
        code += str(stmt.variable)
        code += ' );'
    elif isinstance(stmt, WriteValue):
        code += 'printf("%d\\n", '
        code += str(stmt.variable)
        code += ' );'
    elif isinstance(stmt, WriteString):
        code += 'printf("%s\\n", '
        code += str(stmt.string)
        code += ' );'
    elif isinstance(stmt, Comment):
        code += '// '
        code += str(stmt.string)
    elif isinstance(stmt, Loop):
        code += 'while ('
        code += str(stmt.condition).replace('~', '==')
        code += ') { '
        code += '\n'.join([generate_c(s) for s in stmt.true])
        code += '\n}'
    elif isinstance(stmt, Conditional):
        code += 'if ('
        code += str(stmt.condition).replace('~', '==')
        code += ') { '
        code += generate_c(stmt.true)
        code += '\n} else { '
        code += generate_c(stmt.false)
        code += '\n}'
    elif isinstance(stmt, CompoundStatement):
        for stmt in stmt:
            code += generate_c(stmt)
    else:
        raise Exception(stmt.__class__)

    return code + '\n'


def generator(ast):
    code = '#include <stdio.h>\n' \
           '\n' \
           'int main() {\n' \
           '\t'

    for stmt in ast:
        code += generate_c(stmt)

    return code + '}\n'
