.intel_syntax noprefix

.global main
    .text

_start:
main:
    push rbp
    mov rbp, rsp
mov eax, 15
mov DWORD PTR [rbp-4], eax

mov eax, 13
mov DWORD PTR [rbp-8], eax

mov rax, 1
mov rdi, 1
mov rsi, $STRING_6601026
mov rdx, 27
syscall


mov rax, 1
mov rdi, 1
mov rsi, $STRING_4021463
mov rdx, 28
syscall


mov eax, DWORD PTR [rbp-4]
add eax, DWORD PTR [rbp-8]
mov DWORD PTR [rbp-12], eax


mov eax, 1
mov ebx, 0
int 0x80

STRING_6601026: .string "Enter the first number: "
STRING_4021463: .string "Enter the second number: "
