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

wrapper(main)
