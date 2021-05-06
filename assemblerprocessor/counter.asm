include oneline.asm

Entry_point:
	Mov Ax, 10 
	inc cx
	cmp cx, 5
	jnz a_la_grande_le_puse_cuca
Ciclo:
	Add ax, cx
	Inc cx
	Cmp cx, 3
	Jnz ciclo
