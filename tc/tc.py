import heapq
import numpy as np
import sys
from estadistica import *

#comentarios:
# A continuacion se detalla el esqueleto de la primera parte del trabajo de Teoria de Colas. 
# El modelo que seguiremos es el de un supermercado con una cola y multiples servidores (o cajas de atencion) 
# prefijo de las variables:
#	f: float
#	i: int
#	v*: vector o lista de tipo *
#   c: instancia de una clase

def distribucionExponencial(tasa):
	return (-1/tasa) * np.log(1-np.random.random())

class Cliente:
	def __init__(self, fTiempoLlegada):
		self.tiempoLlegada = fTiempoLlegada
		self.tiempoFinDeAtencion = 0
		self.tiempoInicioAtencion = 0

	def setTiempoInicioAtencion(self,fTiempoInicioAtencion):
		self.tiempoInicioAtencion = fTiempoInicioAtencion
	
	def setTiempoSalida(self, fTiempoSalida):
		self.tiempoFinDeAtencion = fTiempoSalida
		
class Sistema:
	def __init__(self, fTasaLlegadaClientes, vfTasasAtencionServidores):
		self.Lambda = fTasaLlegadaClientes
		self.listaDeMu = vfTasasAtencionServidores
		self.cola = Cola()
		self.servidores = self.creacionServidores()
		self.eventos = []
		self.crearBolsaEventos()
		self.tiempoGlobal = 0
		self.eventoProximoCliente()

	def crearBolsaEventos(self):
		heapq.heapify(self.eventos)

	def agregarEvento(self, evento):
		heapq.heappush(self.eventos, evento)

	def proximoEvento(self):
		evento = heapq.heappop(self.eventos)
		return evento

	def creacionServidores(self):
		listaServidores = [Servidor(mu) for mu in self.listaDeMu]
		return listaServidores
	
	def eventoProximoCliente(self):
		evento = EventoProximoCliente(self, self.tiempoGlobal + distribucionExponencial(self.Lambda))
		self.agregarEvento(evento)

	def ingresoCliente(self): 
		cliente = Cliente(self.tiempoGlobal)
		self.cola.llegaCliente(cliente)
		self.eventoProximoCliente()
		
	def procesar(self):
		Estadistica.cantMediciones += 1
		proximoEvento = self.proximoEvento()
		self.tiempoGlobal = proximoEvento.tiempo
		proximoEvento.procesar()
		
		for servidor in self.servidores:
			if servidor.estaOcupado:
				Estadistica.cantTotalClientesSistema += 1 
			if not servidor.estaOcupado and self.cola.cantClientes():
				proximoCliente = self.cola.proximoCliente()
				if proximoCliente is not None:
					# Este if es para solucionar el caso de que no se contabiliza
					# los clientes cuando no hay nadie en el sistema
					if (self.cola.cantClientes() != 0):
						Estadistica.cantTotalClientesSistema += 1 
					eventoFinAtencion = servidor.inicioAtencion(self.tiempoGlobal, proximoCliente)
					self.agregarEvento(eventoFinAtencion) 
		cantClientesCola = self.cola.cantClientes()
		Estadistica.cantTotalClientesCola += cantClientesCola
		Estadistica.cantTotalClientesSistema += cantClientesCola
	
class Servidor:
	def __init__(self,fTasaAtencionServidor):
		self.mu = fTasaAtencionServidor
		self.estaOcupado = False
		
	def estaOcupado(self):
		return self.estaOcupado
		
	def inicioAtencion(self, fTiempoGlobal, cCliente):
		self.estaOcupado = True
		self.cliente = cCliente
		cCliente.setTiempoInicioAtencion(fTiempoGlobal) 
		eventoFinAtencion = EventoFinAtencion(fTiempoGlobal + distribucionExponencial(self.mu), self)
		Estadistica.tiempoTotalClientesEnCola += cCliente.tiempoInicioAtencion - cCliente.tiempoLlegada
		Estadistica.cantClientesQueEsperaron += 1 
		return eventoFinAtencion

	def finAtencion(self,fTiempo):
		self.cliente.setTiempoSalida(fTiempo)
		Estadistica.tiempoTotalClientesEnSistema += self.cliente.tiempoFinDeAtencion - self.cliente.tiempoLlegada
		Estadistica.cantClientesAtendidos += 1
		self.cliente = None
		self.estaOcupado = False

class Cola:
	def __init__(self):
		self.cola = []

	def cantClientes(self):
		return len(self.cola)

	def llegaCliente(self,cCliente):
		self.cola.append(cCliente)
		
	def proximoCliente(self):
		if self.cantClientes() != 0:
			return self.cola.pop()
		return None


# clase base de los eventos 	
class Evento:
	def __init__(self, fTiempo):
		self.tiempo = fTiempo
		
	# metodo "lower than" para comparar 2 eventos
	def __lt__(self, other):
		return self.tiempo < other.tiempo
	
	# metodo "gerater than" para comparar 2 eventos
	def __gt__(self, other):
		return self.tiempo > other.tiempo

	# metodo abstracto (debe ser implementado por las subclases)
	def procesar(self):
		pass

#evento correspondiente a la futura finalizacion de atencion de un cliente por parte de un servidor
class EventoFinAtencion(Evento):
	def __init__(self, fTiempo, cServidor):
		super().__init__(fTiempo)
		self.servidor = cServidor

	def procesar(self):
		self.servidor.finAtencion(self.tiempo)

#evento correspondiente a la futura llegada del proximo cliente
class EventoProximoCliente(Evento):
	def __init__(self, cSistema, fTiempo):
		super().__init__(fTiempo)
		self.sistema = cSistema

	def procesar(self):
		self.sistema.ingresoCliente()


