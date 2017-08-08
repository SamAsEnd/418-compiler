
.section    .bss

.section     .text
        .globl  main
        .type   main, @function

_start:
main:
    movq    %rsp, %rbp

                    movl    $21, -4(%rbp)
                    

                    movl    $23, -8(%rbp)
                    

                mov     -4(%rbp), %rax
                mov     %rax, %rdi
                mov     $0, %rax
                call writeNumber

                mov     %rax, %rdx
                mov     $1, %rax
                mov     $1, %rdi
                mov     $str, %rsi
                syscall
               

                mov     -8(%rbp), %rax
                mov     %rax, %rdi
                mov     $0, %rax
                call writeNumber

                mov     %rax, %rdx
                mov     $1, %rax
                mov     $1, %rdi
                mov     $str, %rsi
                syscall
               

                mov     $60, %rax
                mov     $0, %rdi
                syscall
            