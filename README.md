# **418** a small procedural language 

## Question **[3.02]**
Design a small procedural language, present the syntax (using **EBNF**), develop its denotational semantics and implement a simple compiler for this language.

The new language should allow to write a simple program below:

```javascript    
var x = 10
var y
...
while x < 1 do
  y = 1
  y = x * y
  x = x - 1
end
```

Note: *the language has nested block structure, scalar variable over the
integers, assignments, conditionals and while loops.*

Hint: *Use GNU C compiler as your backend compiler.*

## Intro
`418` is a simple programming language which can be used to teach underages how to code.

It's simplistic syntax is easy to learn. Please check the `docs/` for a tutorial.

## Requirement
- Python >= 3.4
- GCC >= 4.8 (Optional to build an executable)

## Usage
```
usage: Main.py [-h] (-e | -o OUTPUT) [-s | -c] file

Our '418' language compiler/interpreter

positional arguments:
  file                  The .418 program source code

optional arguments:
  -h, --help            show this help message and exit
  -e, --execute         interpret the given program
  -o OUTPUT, --output OUTPUT
                        the output executable of the file
  -s, --asm             compile to asm
  -c, --c               transpile to c

```

### Notice:
The default compiler(Assembly compiler) have a library in the `libs/` directory.
Please build the lib before using the Assembly compiler.

```
cd libs/ && make && cd ..
```
