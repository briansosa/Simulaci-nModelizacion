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

# bx divisor, cx dividendo, result in ax
division:
    #recibo parametros
    pop dx
    pop cx
    pop bx
    push dx
    #pusheo parametros para no perderlos
    push bx
    push cx
    #hago al dividendo negativo
    push cx
    push -1
    call multiply
    mov dx, ax
    #pull a los parametros
    pop cx
    pop bx
    mov ax, 0
loop_division:
    add bx, dx
    inc ax
    cmp cx, bx
    jnz loop_division
    ret
    

# retorna en ax
sqrt:
    pop ax
    pop bx
    push ax
    dec bx
    mov ax, -1
loop_sqrt:
    inc ax
    push ax
    push bx
    push ax
    push ax
    call multiply
    mov cx, ax
    pop bx
    pop ax
    cmp cx, bx
    jnz loop_sqrt
    ret

