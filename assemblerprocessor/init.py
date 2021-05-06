import sys
from assembler import *
from visualizer import *
from curses import wrapper

HEIGHT = 10
WIDTH = 40

# def main(stdscr):
def main():
    fileName = 'counter.asm'
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    assembler = Assembler()
    assembler.generateExecutable(fileName)

    if (not assembler.hasError()):
        executable = assembler.getExecutable()
        processor = Processor()
        # visualizer = Visualizer(stdscr, HEIGHT, WIDTH)
        # system = System(executable, processor, visualizer)
        system = System(executable, processor, "visualizer")
        system.process()

        # Desactivando el visualizador
        # try:
            # system.process()
        # except Exception as e:
        #     pass
    else:
        print(assembler.getError())
    

# wrapper(main)
main()