import sys
from assembler import *
from log import *
from visualizer import *
from system import *
from curses import wrapper


HEIGHT = 10
WIDTH = 40

def main(stdscr):
    Log.Init()
    fileNames = ''
    if len(sys.argv) >= 2:
        fileNames = sys.argv[1:]
    else:
        print('Not files to process')
        Log.Write('Not files to process')
        return

    assembler = Assembler()
    visualizer = Visualizer(stdscr, HEIGHT, WIDTH)
    processor = Processor(visualizer)
    executables = []
    for fileName in fileNames:
        assembler.generateExecutable(fileName)
        if (not assembler.hasError()):
            executables.append(assembler.getExecutable())
            assembler.clear()
        else:
            print(assembler.getError())
            Log.Write(assembler.getError())
            return

    System.NewSystem(executables, processor)
    processor.executeProcess()

# hacer programa de fibonacci
# programa que encuentre las raices de una funcion cuadratica
# mas funciones matematicas

# division:
# 10/2 - reintento: 0
# 10 - 2 = 8, reintento=1
# 8 - 2 = 6, reintento=2
# 6 - 2 = 4, reintento=3
# 4 - 2 = 2, reintento=4
# 2 - 2 = 0, reintento=5

# 9/2
# 9 - 2 = 7
# 7 - 2 = 5
# 5 - 2 = 3
# 3 - 2 = 1
# 1 - 2 = -1 -> no contar reintento por ser negativo

# 17/9
# 17 - 9 = 8
# 8 - 9 = -1 -> no contar


# (-b +- sq(b^2-4*a*c)) / 2.a

wrapper(main)
