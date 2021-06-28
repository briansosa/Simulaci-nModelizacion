import math

#comentarios:
# A continuacion se detalla el esqueleto de la clase Estadistica del trabajo de Teoria de Colas.
# Esta clase debería ser incorporada al trabajo desarrollado en la primera parte del TP.
# Agregar todos los métodos que sean necesarios para el cálculo de las estadísticas.

# prefijo de las variables:
#	f: float
#	i: int
#	v*: vector o lista de tipo *
#   c: instancia de una clase

class Estadistica:

	tiempoTotalClientesEnSistema = 0
	tiempoTotalClientesEnCola = 0
	cantClientesAtendidos = 0
	cantClientesQueEsperaron = 0
	cantMediciones = 0

	# def __init__(self):
	# 	#acumulador del tiempo total que pasaron los clientes en el sistema
	# 	self.tiempoTotalClientesEnSistema = 0

	# 	#acumulador del tiempo total que pasaron los clientes en la cola
	# 	self.tiempoTotalClientesEnCola = 0

	# 	#acumulador de clientes que fueron atendidos
	# 	self.cantClientesAtendidos = 0

	# 	#acumulador de clientes que esperaron en la cola
	# 	self.cantClientesQueEsperaron = 0

    #     # n?
	# 	self.cantMediciones = 0

    #W: tiempo promedio que paso un cliente en el sistema
	@classmethod
	def W(cls):
		if (cls.cantClientesAtendidos == 0):
			cls.cantClientesAtendidos = 1

		return cls.tiempoTotalClientesEnSistema / cls.cantClientesAtendidos

	#Wq: tiempo promedio que paso un cliente en la cola
	@classmethod
	def Wq(cls):
		if (cls.cantClientesQueEsperaron == 0):
			cls.cantClientesQueEsperaron = 1
		return cls.tiempoTotalClientesEnCola / cls.cantClientesQueEsperaron


	# Las funciones L y Lq las pusimos con el Lambda para ver el resultado aproximado y poder con la visualizacion
	# Ver con que se reemplaza el lambda en cada caso.

	#L: promedio de clientes en el sistema
	@classmethod
	def L(cls, sistema):
		return sistema.Lambda * cls.W()

	#Lq: promedio de clientes en la cola
	@classmethod
	def Lq(cls, sistema):
		return sistema.Lambda * cls.Wq()
