import time
import curses
from curses import wrapper
from visual import *
from estadistica import *
from tc import *

def iniciar():
	#1) inicialización de variables
	#2.1) crear instancia de estadistica
	#2.2) crear instancia de sistema
	#3) llegada 1er. cliente
        
    # se le pasa lambda y mu
    Lambda = 0.5
    mus = [0.2, 0.2, 0.2]
    # estadistica = Estadistica()

    sistema = Sistema(Lambda, mus)
    sistema.procesar()

    print("W")
    print(Estadistica.W())

    print("Wq")
    print(Estadistica.Wq())

    print("L")
    print(Estadistica.L(sistema))

    print("Lq")
    print(Estadistica.Lq(sistema))

	# imprimirTitulo(screen)

	# imprimirDatos(screen)

	# terminar = False

	# i = 0
	# while(not terminar):
	# 	screen.nodelay(True)

	# 	#sistema.procesar()

	# 	#estadistica.procesar()

	# 	actualizarEstadoServidores(screen,i % 2 == 0)

	# 	time.sleep(0.5)

	# 	i += 1
	# 	#terminar con la tecla "f"
	# 	if (screen.getch() == ord('f')):
	# 		terminar = True

# wrapper(iniciar)
iniciar()