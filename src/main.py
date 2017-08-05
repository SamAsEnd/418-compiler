import os

from src.lib.tokenizer import tokenize
from src.lib.parser import parse
from src.lib.generator import generator


def main():
    content = open('../sample/sample.418', 'r').read()

    tokens = []

    for line in content.splitlines():
        line = line.lstrip().rstrip()
        if len(line) > 0:
            tokens.append(tokenize(line))

    ast = parse(tokens)
    code = generator(ast)
    print(code);
    open('test.c', 'w').write(code)
    os.system('gcc test.c -o test')
    print('done')


if __name__ == '__main__':
    main()
