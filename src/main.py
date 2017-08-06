#!/bin/env python3

import os
import sys
import argparse
import tempfile

from lib.tokenizer import tokenize
from lib.parser import parse
from lib.gen_asm import generator


def main():
    p = argparse.ArgumentParser(description="Our '418' language compiler/interpreter")
    p.add_argument('file', help="The .418 program source code")
    p.add_argument('-o', '--output', help="The output executable of the file")
    args = p.parse_args()

    try:
        tokens = tokenize(open(args.file, 'r').read())
        tree = parse(tokens)
        code = generator(tree)
        # code = code.replace('PTR', ' ')
        code = code.replace('ebp', 'rbp')
        # print(code)
        # exit(0)

        f = open('temp.s', 'w')  # tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.asm')
        f.write(code)
        f.close()

        os.system('gcc -c "%s" -o "%s"' % (f.name, args.output + '.o'))
        # os.system('nasm -f elf %s -o %s' % (f.name, args.output + '.o'))

        os.system('ld %s' % (args.output + '.o'))
        # os.unlink(f.name)
        # os.unlink(args.output + '.o')
        exit(0)
    except SyntaxError as se:
        sys.stderr.write('Exception: ' + se.msg)
        exit(1)


if __name__ == '__main__':
    main()
