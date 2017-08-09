from lib.nodes import *


def compile_statement(stmt: Statement):
    if isinstance(stmt, VarDeclare):
        return 'int %s = %s;\n' % (str(stmt.variable), str(stmt.expression))
    elif isinstance(stmt, Assignment):
        return '%s = %s;\n' % (str(stmt.variable), str(stmt.expression))
    elif isinstance(stmt, Read):
        return 'scanf("%%d", &%d);\n' % (str(stmt.variable))
    elif isinstance(stmt, WriteValue):
        return 'printf("%%d", %d);\n' % (str(stmt.variable))
    elif isinstance(stmt, WriteString):
        return 'printf("%%s", %s);\n' % stmt.string
    elif isinstance(stmt, Comment):
        return '// %s\n' % stmt.string
    elif isinstance(stmt, Loop):
        return """
                while (%s) {
                    %s
                }
                """ % (str(stmt.condition).replace('~', '=='), compile_statement(stmt.true))
    elif isinstance(stmt, Conditional):
        return """
                if (%s) {
                    %s
                } else {
                    %s
                }
                """ % (str(stmt.condition).replace('~', '=='),
                       compile_statement(stmt.true),
                       compile_statement(stmt.false))
    elif isinstance(stmt, CompoundStatement):
        code = ''
        for stmt in stmt:
            code += compile_statement(stmt)
        return code
    else:
        raise Exception(stmt.__class__)


def compile_it(tree):
    code = """
            #include <stdio.h>
            int main() {  
           """

    for stmt in tree:
        code += compile_statement(stmt)

    code += '\n}\n'

    return code


def build(code, args):
    pass
