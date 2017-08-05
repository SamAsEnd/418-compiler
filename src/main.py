#!/bin/env python3

import os
import sys
import argparse
import tempfile

from lib.tokenizer import tokenize
from lib.parser import parse
from lib.generator import generator


def main():
    p = argparse.ArgumentParser(description="Our '418' language compiler/interpreter")
    p.add_argument('file', help="The .418 program source code")
    p.add_argument('-o', '--output', help="The output executable of the file")
    args = p.parse_args()

    try:
        tokens = tokenize(open(args.file, 'r').read())
        tree = parse(tokens)
        code = generator(tree)

        f = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.c')
        f.write(code)
        f.close()

        os.system('gcc "%s" -o "%s"' % (f.name, args.output))
        os.unlink(f.name)
        exit(0)
    except SyntaxError as se:
        sys.stderr.write('Exception: ' + se.msg)
        exit(1)


if __name__ == '__main__':
    main()
