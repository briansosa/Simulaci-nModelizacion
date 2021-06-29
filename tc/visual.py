# Este es un programa de ejemplo de cómo debería incorporarse la visualización del sistema de Teoría de Colas desarrollado en la primera parte del TP
# Modificar y completar todo lo que consideren necesario
from estadistica import *


def imprimirTitulo(screen):
	screen.addstr(0,0,'Servidores (X = ocupado, " " = desocupado)')

def imprimirDatos(screen, sistema):
	servidores = len(sistema.servidores)

	fila = 1
	columna = 1
	for i in range(servidores):
		screen.addstr(fila,columna,'{:02d}: |   | '.format(i))
		if fila % servidores == 0:
			fila = 1
			columna += 20
		else:
			fila += 1
	actualizarVariablesEstadistica(screen, sistema)



def actualizarEstadoServidores(screen,sistema):
	servidores = sistema.servidores
	fila = 1
	columna = 7
	for servidor in servidores:
		if servidor.estaOcupado:
			screen.addstr(fila,columna,'X')
		else:
			screen.addstr(fila,columna,' ')
		if fila % len(servidores) == 0:
			fila = 1
			columna += 20
		else:
			fila += 1
	
	actualizarVariablesEstadistica(screen, sistema)
	

def actualizarVariablesEstadistica(screen, sistema):
	screen.addstr(7,0,'Cantidad de clientes en espera (en la cola): {:02d}'.format(sistema.cola.cantClientes()))
	screen.addstr(8,0,'Cantidad de mediciones: {}'.format(Estadistica.cantMediciones))
	screen.addstr(9,0,'Tiempo global: {}'.format(sistema.tiempoGlobal))
	screen.addstr(10,0,'L: {}'.format(Estadistica.L()))
	screen.addstr(11,0,'Lq: {}'.format(Estadistica.Lq()))
	screen.addstr(10,50,'W: {}'.format(Estadistica.W()))
	screen.addstr(11,50,'Wq: {}'.format(Estadistica.Wq()))