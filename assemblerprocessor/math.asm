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
    

# por ahora retorna en dx, pero le falta refinar
sqrt:
    pop ax
    pop bx
    push ax
    dec bx
    mov ax, 0
loop_sqrt:
    mov dx, ax
    push bx
    push ax
    push ax
    call multiply
    pop bx
    cmp ax, bx
    inc ax
    jnz loop_sqrt
    ret

