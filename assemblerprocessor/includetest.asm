juanita:
    pop cx
    pop dx
    push cx
    inc dx
    ret

Entry_point:
    push 1
    call juanita
    mov ax, 3