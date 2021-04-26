import sys
from assembler import *

def main():
    fileName = 'counter.asm'
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    assembler = Assembler()
    assembler.generateExecutable(fileName)
    assembler.process()

main()