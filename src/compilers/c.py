from lib.nodes import *


def transpile_statement(stmt: Statement) -> str:
    """
    Convert a given statement node to a c code
    
    :param stmt: the statement from the abstract syntax tree 
    :return: str the valid c code
    """
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
                """ % (str(stmt.condition).replace('~', '=='), transpile_statement(stmt.true))
    elif isinstance(stmt, Conditional):
        return """
                if (%s) {
                    %s
                } else {
                    %s
                }
                """ % (str(stmt.condition).replace('~', '=='),
                       transpile_statement(stmt.true),
                       transpile_statement(stmt.false))
    elif isinstance(stmt, CompoundStatement):
        code = ''
        for stmt in stmt:
            code += transpile_statement(stmt)
        return code
    else:
        raise SyntaxError(stmt.__class__ + ' not implemented!')


def transpile(tree: CompoundStatement) -> str:
    code = """
            #include <stdio.h>
            int main() {  
           """

    for stmt in tree:
        code += transpile_statement(stmt)

    code += '\n}\n'

    return code
