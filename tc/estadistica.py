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

	cantTotalClientesSistema = 0
	cantTotalClientesCola = 0

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


	#L: promedio de clientes en el sistema
	@classmethod
	def L(cls):
		if (cls.cantMediciones == 0):
			cls.cantMediciones = 1
		return cls.cantTotalClientesSistema/cls.cantMediciones

	#Lq: promedio de clientes en la cola
	@classmethod
	def Lq(cls):
		if (cls.cantMediciones == 0):
			cls.cantMediciones = 1
		return cls.cantTotalClientesCola/cls.cantMediciones
