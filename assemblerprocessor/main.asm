include math.asm

entry_point:
    push 4
    call sqrt
    push ax
    mov ax, 0
    mov bx, 0
    mov cx, 0
    mov dx, 0
    push 4
    push -2
    call multiply
    push ax
    mov ax, 0
    mov bx, 0
    mov cx, 0
    mov dx, 0
    push 9
    push 3
    call division
    push ax
    mov ax, 0
    mov bx, 0
    mov cx, 0
    mov dx, 0
    # resultado division
    pop cx
    # resultado multiplicacion
    pop bx
    # resultado raiz
    pop ax
