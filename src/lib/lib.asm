.intel_syntax noprefix

.section .data

number: .zero 4
buffer: .zero 15

.text
    .globl main

int2str:
  push rbp
  mov rbp, rsp
  mov QWORD PTR [rbp-24], rdi
  mov DWORD PTR [rbp-28], esi
  mov DWORD PTR [rbp-16], 10
  mov rax, QWORD PTR [rbp-24]
  mov QWORD PTR [rbp-8], rax
  mov eax, DWORD PTR [rbp-28]
  mov DWORD PTR [rbp-12], eax
.L3:
  cmp DWORD PTR [rbp-12], 0
  jle .L2
  mov ecx, DWORD PTR [rbp-12]
  mov edx, 1717986919
  mov eax, ecx
  imul edx
  sar edx, 2
  mov eax, ecx
  sar eax, 31
  sub edx, eax
  mov eax, edx
  mov DWORD PTR [rbp-12], eax
  add QWORD PTR [rbp-8], 1
  jmp .L3
.L2:
  mov QWORD PTR [rbp-8], 0
  #mov rax, QWORD PTR [rbp-8]
  #mov BYTE PTR [rax], 0
.L5:
  mov rax, QWORD PTR [rbp-8]
  cmp rax, QWORD PTR [rbp-24]
  jne .L4
  sub QWORD PTR [rbp-8], 1
  mov ecx, DWORD PTR [rbp-28]
  mov edx, 1717986919
  mov eax, ecx
  imul edx
  sar edx, 2
  mov eax, ecx
  sar eax, 31
  sub edx, eax
  mov eax, edx
  add eax, 48
  mov edx, eax
  mov BYTE PTR [rbp-8], dl
  mov ecx, DWORD PTR [rbp-28]
  mov edx, 1717986919
  mov eax, ecx
  imul edx
  sar edx, 2
  mov eax, ecx
  sar eax, 31
  sub edx, eax
  mov eax, edx
  mov DWORD PTR [rbp-28], eax
  add DWORD PTR [rbp-12], 1
  jmp .L5
.L4:
  mov eax, DWORD PTR [rbp-12]
  pop rbp
  ret

str2int:
  push rbp
  mov rbp, rsp
  mov QWORD PTR [rbp-24], rdi
  mov DWORD PTR [rbp-28], esi
  mov DWORD PTR [rbp-4], 0
  mov rax, QWORD PTR [rbp-24]
  mov QWORD PTR [rbp-16], rax
.L9:
  mov rax, QWORD PTR [rbp-16]
  movzx eax, BYTE PTR [rax]
  test al, al
  je .L8
  mov edx, DWORD PTR [rbp-4]
  mov eax, edx
  sal eax, 2
  add eax, edx
  add eax, eax
  mov DWORD PTR [rbp-4], eax
  mov rax, QWORD PTR [rbp-16]
  movzx eax, BYTE PTR [rax]
  movsx eax, al
  sub eax, 48
  add DWORD PTR [rbp-4], eax
  add QWORD PTR [rbp-16], 1
  jmp .L9
.L8:
  mov eax, DWORD PTR [rbp-4]
  pop rbp
  ret

main:
  push rbp
  mov rbp, rsp
