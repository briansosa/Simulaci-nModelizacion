import time
import sys
from copy import copy, deepcopy
from curses import wrapper

MAX_HEIGHT, MAX_WIDHT = 25, 25
ALIVE_CHARACTER = 'X'
DEAD_CHARACTER = ' '
LIMIT_CHARACTER = '*'
SLEEP_SECONDS = 0.25
NEIGHBORS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
DEFAULT_CONFIG = "blinker.txt"

def main(stdscr):
  initTerminal(stdscr)

  fileName = DEFAULT_CONFIG

  if len(sys.argv) >= 2:
      fileName = sys.argv[1]

  config = readFile(fileName)

  matrix = initMatrix(config)
  showMatrix(stdscr, matrix)

  nextGenerationFlag = False
  while True:
    c = stdscr.getch()
    if c == ord('q'):
      break
    elif c == ord('b') or nextGenerationFlag:
        matrix = nextGeneration(matrix)
        showMatrix(stdscr, matrix)
        nextGenerationFlag = True
        time.sleep(SLEEP_SECONDS)

# Método que se encarga de inicializar la matriz con los limites y los datos iniciales
def initMatrix(initConfig):
    # Se agrega una fila y columna extra para poner los límites.
    # TODO: Falta validar la longitud maxima del array dependiendo los limites de la terminal.
    matrix = [[DEAD_CHARACTER for x in range(MAX_WIDHT + 2)] for y in range(MAX_HEIGHT + 2)]
    fillLimits(matrix)
    fillMatrix(matrix, initConfig)
    return matrix


# Método que se encarga de agregar las celulas vivas a partir de los datos iniciales
def fillMatrix(matrix, config):
    for aliveCell in config:
        (rowAliveCell, columnAliveCell) = aliveCell
        matrix[rowAliveCell + 1][ columnAliveCell + 1] = ALIVE_CHARACTER

# Método que se encarga de llenar todos los límites de la matriz
def fillLimits(matrix):
    # Ingresa los limites de la primer fila
    for i in range(MAX_WIDHT + 2):
        matrix[0][i] = LIMIT_CHARACTER

    # Ingresa los limites de la última fila
    for i in range(MAX_WIDHT + 2):
        matrix[MAX_HEIGHT + 1][i] = LIMIT_CHARACTER

    # Ingresa los limites de la primer columna
    for i in range(MAX_HEIGHT + 2):
        matrix[i][0] = LIMIT_CHARACTER

    # Ingresa los limites de la ultima columna
    for i in range(MAX_HEIGHT + 2):
        matrix[i][MAX_WIDHT + 1] = LIMIT_CHARACTER 

# Se encarga de procesar la siguiente generación. Hace una copia de la matriz actual, para poder reemplazar los datos
def nextGeneration(matrix):
    nextGenerationMatrix = deepcopy(matrix)
    for indexRow, row in enumerate(matrix):
        for indexColumn in range(len(row)):
            position = (indexRow, indexColumn)
            if matrix[position[0]][position[1]] != LIMIT_CHARACTER:
                neighbords = findNeighbors(position)
                liveCellCount = getLivingCells(matrix, neighbords)
                updateCellState(nextGenerationMatrix, position, liveCellCount)
    return nextGenerationMatrix
    
# Obtiene todas las posiciones vecinas de cualquier direccion de la matriz.
# Ej: si estamos en la posicion (3,3) va a retornar [(2,2), (3,2), (4,2), (2,3), (4,3), (2,4), (3,4), (4,4)]
def findNeighbors(position):
    neighbords = [tuple(map(sum, zip(nei, position))) for nei in NEIGHBORS]
    return neighbords

# Define las reglas del juego, actualiza el estado de una celda dependiendo sus vecinos.
def updateCellState(nextGenerationMatrix, position, liveCellCount):
    if nextGenerationMatrix[position[0]][position[1]] == DEAD_CHARACTER and liveCellCount == 3:
        nextGenerationMatrix[position[0]][position[1]] = ALIVE_CHARACTER
    elif nextGenerationMatrix[position[0]][position[1]] == ALIVE_CHARACTER and not (liveCellCount == 2 or liveCellCount == 3):
        nextGenerationMatrix[position[0]][position[1]] = DEAD_CHARACTER

# Obtiene el numero de celulas vecinas vivas
def getLivingCells(nextGenerationMatrix, neighbords):
    aliveCells = list(filter(lambda x: (nextGenerationMatrix[x[0]][x[1]] == ALIVE_CHARACTER), neighbords))
    return len(aliveCells)

def initTerminal(stdscr):
  stdscr.nodelay(True)
  stdscr.clear()

def showMatrix(stdscr, matrix):
  for indexRow, row in enumerate(matrix):
    for indexColumn in range(len(row)):
      stdscr.addch(indexRow, indexColumn, matrix[indexRow][indexColumn])
  stdscr.refresh()

def readFile(fileName):
  with open(fileName) as f:
      lines = [lineToTuple(line.rstrip()) for line in f]
  return lines

def lineToTuple(line):
  splitLine = line.split(',')
  return (int(splitLine[0]), int(splitLine[1]))


wrapper(main)