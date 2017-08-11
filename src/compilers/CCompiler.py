import os
import tempfile

from compilers.Compiler import Compiler
from nodes import *


class CCompiler(Compiler):
    def __init__(self, tree: CompoundStatement) -> None:
        super().__init__(tree)
        self.code = ''

    def transpile_statement(self, stmt: Statement) -> str:
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
            return 'scanf("%%d", &%s);\n' % (str(stmt.variable))
        elif isinstance(stmt, WriteValue):
            return 'printf("%%d", %s);\n' % (str(stmt.variable))
        elif isinstance(stmt, WriteString):
            return 'printf("%%s", %s);\n' % stmt.string
        elif isinstance(stmt, Comment):
            return '// %s\n' % stmt.string
        elif isinstance(stmt, Loop):
            return """
                    while (%s) {
                        %s
                    }
                    """ % (
            str(stmt.condition).replace('~', '==').replace('!', '!='), self.transpile_statement(stmt.true))
        elif isinstance(stmt, Conditional):
            return """
                    if (%s) {
                        %s
                    } else {
                        %s
                    }
                    """ % (str(stmt.condition).replace('~', '==').replace('!', '!='),
                           self.transpile_statement(stmt.true),
                           self.transpile_statement(stmt.false))
        elif isinstance(stmt, CompoundStatement):
            code = ''
            for stmt in stmt:
                code += self.transpile_statement(stmt)
            return code
        else:
            raise SyntaxError(stmt.__class__ + ' not implemented!')

    def compile(self):
        code = """
                #include <stdio.h>
                int main() {  
               """

        for stmt in self.tree:
            code += self.transpile_statement(stmt)

        self.code = code + '\n}\n'

    def build(self, args):
        if not args.c:
            c_file = tempfile.NamedTemporaryFile(mode='w', suffix='.c')
        else:
            c_file = open(args.output + '.c', 'w')

        c_file.write(self.code)
        c_file.close()

        if args.output is not None:
            # assemble the asm
            status = os.system('gcc -g %s -o %s' % (c_file.name, args.output))

            if status != 0:
                raise RuntimeError('gcc: compiler failed with exit code ' + str(status))
