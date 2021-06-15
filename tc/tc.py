import heapq
import numpy as np
import sys


#comentarios:
# A continuacion se detalla el esqueleto de la primera parte del trabajo de Teoria de Colas. 
# El modelo que seguiremos es el de un supermercado con una cola y multiples servidores (o cajas de atencion) 
# prefijo de las variables:
#	f: float
#	i: int
#	v*: vector o lista de tipo *
#   c: instancia de una clase

def distribucionExponencial(lamda):
	return (-1/lamda) * np.log(1-np.random.random())

class Cliente:
	def __init__(self, fTiempoLlegada):
		self.tiempoLlegada = fTiempoLlegada

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

	def crearBolsaEventos(self):
		heapq.heapify(self.eventos)

	def agregarEvento(self, evento):
		print(f"agrego evento con tiempo: {evento.tiempo}")
		heapq.heappush(self.eventos, evento)

	def proximoEvento(self):
		evento = heapq.heappop(self.eventos)
		print(f"pop proximo evento: {evento.tiempo}")
		return evento

	def creacionServidores(self):
		listaServidores = [Servidor(mu) for mu in self.listaDeMu]
		return listaServidores
	
	def eventoProximoCliente(self):
		evento = EventoProximoCliente(self, self.tiempoGlobal + distribucionExponencial(self.Lambda))
		print(f"creo evento proximo evento: {evento.tiempo}")
		return evento
	
	def ingresoCliente(self): 
		cliente = Cliente(self.tiempoGlobal)
                    	 ## Es el tiempo global?
		self.cola.llegaCliente(cliente)
		self.agregarEvento(self.eventoProximoCliente())
		
	def procesar(self):
		primerEvento = self.eventoProximoCliente()
		self.agregarEvento(primerEvento)
		while (True):
			proximoEvento = self.proximoEvento()
			self.tiempoGlobal = proximoEvento.tiempo
			proximoEvento.procesar()
			for servidor in self.servidores:
				if not servidor.estaOcupado and self.cola.cantClientes():
					print("voy a atender a un cliente")
					proximoCliente = self.cola.proximoCliente()
					if proximoCliente is not None:
						print("inicio atencion")
						eventoFinAtencion = servidor.inicioAtencion(self.tiempoGlobal, proximoCliente)
						self.agregarEvento(eventoFinAtencion)       

	
class Servidor:
	def __init__(self,fTasaAtencionServidor):
		self.mu = fTasaAtencionServidor
		self.estaOcupado = False
		
	def estaOcupado(self):
		return self.estaOcupado
		
	def inicioAtencion(self, fTiempoGlobal,cCliente):
		self.estaOcupado = True
		self.cliente = cCliente
		cCliente.setTiempoInicioAtencion(fTiempoGlobal) 
		eventoFinAtencion = EventoFinAtencion(fTiempoGlobal + self.mu, self) 
		return eventoFinAtencion

	def finAtencion(self,fTiempo):
		self.cliente.setTiempoSalida(fTiempo)
		self.cliente = None
		self.estaOcupado = False

class Cola:
	def __init__(self):
		self.cola = []

	def cantClientes(self):
        # return len(self.cola)
		length = len(self.cola)
		if length > 10:
			sys.exit()
		else:
			return length

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
                                ## es este tiempo??????????

#evento correspondiente a la futura llegada del proximo cliente
class EventoProximoCliente(Evento):
	def __init__(self, cSistema, fTiempo):
		super().__init__(fTiempo)
		self.sistema = cSistema

	def procesar(self):
		self.sistema.ingresoCliente()

# se le pasa lambda y mu
sistema = Sistema(0.5, [0.2, 0.2, 0.2])
sistema.procesar()
