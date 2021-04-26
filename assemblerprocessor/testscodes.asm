Entry_point:
	Mov flag, 0
    jnz for_hasta_diez_en_ax 
Etiqueta_falopa:
    mov ax, 80
for_hasta_diez_en_ax:
	inc ax
    cmp ax, 9
    jnz for_hasta_diez_en_ax