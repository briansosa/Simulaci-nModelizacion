import time
import curses
from curses import wrapper
from visual import *
from tc import *

def iniciar(screen):
	Lambda = 0.5
	mus = [0.2, 0.2, 0.2]

	sistema = Sistema(Lambda, mus)

	imprimirTitulo(screen)
	imprimirDatos(screen, sistema)

	terminar = False

	i = 0
	while(not terminar):
		screen.nodelay(True)
		sistema.procesar()
		actualizarEstadoServidores(screen, sistema)

		time.sleep(0.003)

		i += 1
		#terminar con la tecla "f"
		if (screen.getch() == ord('f')):
			terminar = True

wrapper(iniciar)
