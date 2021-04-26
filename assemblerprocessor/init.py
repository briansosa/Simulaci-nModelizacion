import sys
from assembler import *

def main():
    fileName = 'counter.asm'
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    assembler = Assembler()
    assembler.generateExecutable(fileName)

    if (not assembler.hasError()):
        system = System(assembler.getExecutable(), Processor())
        system.process()
    else:
        print(assembler.getError())

main()