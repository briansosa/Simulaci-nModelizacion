import sys
import re
from abc import ABC, abstractmethod

VALID_INSTRUCCION = ['mov', 'add', 'jmp', 'jnz', 'cmp', 'inc', 'dec']

class Ensamblador:
    def __init__(self):
        self.errors = []

    def process(self, filename):
        ejecutable = Ejecutable()
        with open(filename) as file:
            ejecutable.setSourceCode([self.cleanLine(line) for line in file])
            # indexInstruction no deberia ser el código fuente porque en ese codigo esta contemplado los labels y esta mal, deberia
            # agregarse al lookup table solo el indice de la intrucción 
            for indexInstruction, line in enumerate(ejecutable.getSourceCode()):
                if self.isLabel(line):
                    label = self.getLabel(line)
                    ejecutable.addToLookupTable(label, indexInstruction)
                elif self.isInstruction(line):
                    instructionName, parameters = self.parseInstruction(line)
                    instruction = self.generateInstruction(instructionName, parameters)
                    print(instruction)


    def generateInstruction(self, instructionName, parameters):
        listParams = self.parseParameters(parameters)
        if len(listParams) == 1:
            if instructionName == 'jmp':
                return Jmp(listParams[0])
            elif instructionName == 'jnz':
                return Jnz(listParams[0])
            elif instructionName == 'inc':
                return Inc(listParams[0])
            elif instructionName == 'dec':
                return Dec(listParams[0])
        elif len(listParams) == 2:
            if instructionName == 'mov':
                return Mov(listParams[0], listParams[1])
            elif instructionName == 'add':
                return Add(listParams[0], listParams[1])
            elif instructionName == 'cmp':
                return Cmp(listParams[0], listParams[1])
    
    def parseParameters(self, parameters):
        parametersList = []
        oneParamRegex = '^(\w+)\s*$'
        twoParamRegex = '^(\w+)\s*,\s*(\w+)\s*$'
        oneParamMatch = re.search(oneParamRegex, parameters)
        if oneParamMatch:
            parametersList.append(oneParamMatch.group(1))
        else:
            twoParamMatch = re.search(twoParamRegex, parameters)
            if twoParamMatch:
                parametersList.append(twoParamMatch.group(1))
                parametersList.append(twoParamMatch.group(2))

        return parametersList

    def isLabel(self, line):
        match = re.search('^([\w_]+):$', line)
        return match

    def getLabel(self, line):
        match = re.search('^([\w_]+):$', line)
        return match.group(1)

    def isInstruction(self, line):
        match = re.search('^(mov|add|cmp|inc|dec|jmp|jnz)\s+([\w_,\s]+)', line)
        return match and match.group(1) in VALID_INSTRUCCION
    
    def parseInstruction(self, line):
        match = re.search('^(mov|add|cmp|inc|dec|jmp|jnz)\s+([\w_,\s]+)', line)
        return (match.group(1), match.group(2))


    def cleanLine(self, line):
        line = line.strip()
        line = line.replace('\t', '')
        line = line.replace('\n', '')
        line = line.lower()
        return line    

class Ejecutable:
    def __init__(self):
        self.entryPoint = 0
        self.instructions = []
        self.lookupTable = dict()
        self.sourceCode = []

    def process(self, filename):
        pass

    def setSourceCode(self, sourceCode):
        self.sourceCode = sourceCode

    def getSourceCode(self):
        return self.sourceCode

    def addToLookupTable(self, key, value):
        self.lookupTable[key] = value


class Instruccion(ABC):    
    @abstractmethod
    def procesar(self, procesador):
        pass

class Mov(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def procesar(self, procesador):
        pass

class Add(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def procesar(self, procesador):
        pass

class Cmp(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def procesar(self, procesador):
        pass

class Jmp(Instruccion):
    def __init__(self, param):
        self.param = param

    def procesar(self, procesador):
        pass

class Jnz(Instruccion):
    def __init__(self, param):
        self.param = param

    def procesar(self, procesador):
        pass

class Inc(Instruccion):
    def __init__(self, param):
        self.param = param

    def procesar(self, procesador):
        pass

class Dec(Instruccion):
    def __init__(self, param):
        self.param = param

    def procesar(self, procesador):
        pass


def main():
    filename = 'counter.asm'
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]

    ensamblador = Ensamblador()
    ensamblador.process(filename)

main()