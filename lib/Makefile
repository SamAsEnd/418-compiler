
all: clean
	gcc -ffreestanding -fno-builtin -c lib418.c -o lib418.o

debug: clean
	gcc -save-temps -ffreestanding -fno-builtin -g -c lib418.c -o lib418.o

clean:
	-@rm -rf lib418.i lib418.s lib418.o 2> /dev/null || true
