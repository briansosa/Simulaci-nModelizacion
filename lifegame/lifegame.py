from copy import copy, deepcopy

MAX_HEIGHT, MAX_WIDHT = 5, 4
# Oscillator - Blinker
# Las configuraciones deben empezar de las coordenadas (1,1)
TEST_DATA = [(1, 1), (2, 1), (3, 1)]
ALIVE_CHARACTER = 'X'
DEAD_CHARACTER = ' '
LIMIT_CHARACTER = '*'
NEIGHBORS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

def main():
    # Inicializar array
    matrix = initMatrix(TEST_DATA)
    print('INIT MATRIX')
    print(matrix)
    # Inicializar CLI
    # Por ahora solo avanza 3 generaciones, para pruebas.
    for i in range(0, 4):
        matrix = nextGeneration(matrix)
        print()
        print('NEXT GENERATION MATRIX: ' + str(i + 1))
        print(matrix)
        #   Actualizo pantalla por cada generacion procesada


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


main()