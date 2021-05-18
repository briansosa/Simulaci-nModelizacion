# Resultado en ax
multiply:
    pop ax
    pop bx
    pop cx
    push ax
    mov ax, 0
loop_multiply:
    add ax, bx
    dec cx
    cmp 1, cx
    jnz loop_multiply
    ret

