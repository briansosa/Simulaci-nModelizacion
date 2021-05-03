Entry_point:
	Mov dx, 1
    jnz for_hasta_diez_en_ax
for_hasta_diez_en_ax:
	inc ax
	dec ax
	inc ax
	dec bx
    mov dx, 10
	inc cx
	inc ax
    inc dx
	inc ax
    cmp ax, 10
    jnz for_hasta_diez_en_ax
    