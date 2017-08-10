#!/bin/env python3

import os
import sys
import argparse

from lib.parser import parse
from lib.tokenizer import tokenize
from compilers.assembly import compile_it, build_it


def main():
    p = argparse.ArgumentParser(description="Our '418' language compiler/interpreter")

    p.add_argument('file', help='The .418 program source code')

    group = p.add_mutually_exclusive_group()
    group.add_argument('-e', '--execute', help='interpret the given program', action='store_true')
    group.add_argument('-o', '--output', help='the output executable of the file', default='a.out')

    p.add_argument('-a', '--asm', help="compile to asm")
    p.add_argument('-c', '--c', help="transcript to c")

    args = p.parse_args()

    try:
        content = open(args.file, 'r').read()
        tokens = tokenize(content)
        tree = parse(tokens)

        code = compile_it(tree)

        if args.asm is not None:
            open(args.asm, 'w').write(code)

        if args.c is not None:
            open(args.c, 'w').write(code)

        if args.output:
            build_it(code, args)
        else:
            pass
            # interpret(tree)


    except SyntaxError as se:
        sys.stderr.write('Exception: ' + se.msg)
        exit(1)


if __name__ == '__main__':
    main()
