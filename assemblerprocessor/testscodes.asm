Entry_point:
	Mov dx, 1
    jnz for_hasta_diez_en_ax
Etiqueta_prueba:
    mov ax, 80
for_hasta_diez_en_ax:
	inc ax
    cmp ax, 10
    jnz for_hasta_diez_en_ax
    dec ax
    add bx, 50
    