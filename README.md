# 418 Small Procedural Language

**[3.02]** **[20pt]** 

Design a small procedural language, present the syntax (using EBNF), develop its denotational semantics and implement a simple compiler forthis language.

The new language should allow to write a simple program below:
    
    var x = 10
    var y
    ...
    while x < 1 do
    y = 1
    y = x*y
    x = x -1
    end
    
Note: the language has nested block structure, scalar variable over the
integers, assignments, conditionals and while loops.

Hint: Use GNU C compiler as your backend compiler.

## Run
    python3 ./src/main.py sample/hello_world.418 -o hello_world
    ./hello_world
