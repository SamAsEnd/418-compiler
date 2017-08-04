import os
import pprint
from pprint import pprint

from generator import generator

from src.parser import parse
from src.tokenizer import tokenize


def main():
    content = open('../sample/sample.418', 'r').read()

    tokens = []

    for line in content.splitlines():
        line = line.lstrip().rstrip()
        if len(line) > 0:
            tokens.append(tokenize(line))

    ast = parse(tokens)
    # exit(0)
    code = generator(ast)
    open('test.c', 'w').write(code)
    os.system('gcc test.c -o test')
    print('done')


if __name__ == '__main__':
    main()
