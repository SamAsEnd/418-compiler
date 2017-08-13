#!/bin/env python3

import sys
import argparse

from Parser import Parser
from Tokenizer import Tokenizer
from compilers.AssemblyCompiler import AssemblyCompiler

from compilers.CCompiler import CCompiler
from compilers.PythonInterpreter import PythonInterpreter


def main():
    p = argparse.ArgumentParser(description="Our '418' language compiler/interpreter")

    p.add_argument('file', help='The .418 program source code')

    group1 = p.add_mutually_exclusive_group(required=True)
    group1.add_argument('-e', '--execute', help='interpret the given program', action='store_true')
    group1.add_argument('-o', '--output', help='the output executable of the file')

    group2 = p.add_mutually_exclusive_group()
    group2.add_argument('-s', '--asm', help="compile to asm", action='store_true')
    group2.add_argument('-c', '--c', help="transpile to c", action='store_true')

    args = p.parse_args()

    try:
        content = open(args.file, 'r').read()
        tokens = Tokenizer.tokenize(content)
        tree = Parser.parse(tokens)

        if args.execute:
            compiler = PythonInterpreter(tree)
        elif args.c:
            compiler = CCompiler(tree)
        else:
            compiler = AssemblyCompiler(tree)

        compiler.compile()
        compiler.build(args)
    except Exception as e:
        raise e


if __name__ == '__main__':
    main()
