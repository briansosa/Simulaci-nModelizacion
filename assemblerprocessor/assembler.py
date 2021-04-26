from executable import *
from instruction import *
from processor import *
from system import *
import re

VALID_INSTRUCCION = ['mov', 'add', 'jmp', 'jnz', 'cmp', 'inc', 'dec']
COMMENT = "#"

class Assembler:
    def __init__(self):
        self.errors = []
        self.executable = Executable()
        self.instructionsToReplace = []

    def generateExecutable(self, filename):
        with open(filename) as file:
            self.executable.setSourceCode([self.cleanLine(line) for line in file])

        indexInstruction = 0
        for indexSourceCode, line in enumerate(self.executable.getSourceCode()):
            if len(line) == 0 or line[0] == COMMENT:
                continue
            elif self.isLabel(line):
                label = self.getLabel(line)
                self.executable.addToLookupTable(label, indexInstruction)
            elif self.isInstruction(line):
                instructionName, parameters = self.parseInstruction(line)
                instruction = self.generateInstruction(instructionName, parameters)
                self.executable.addToInstructions(instruction)
                if isinstance(instruction, Jmp) or isinstance(instruction, Jnz):
                    self.instructionsToReplace.append(indexInstruction)

                indexInstruction += 1
        self.executable.setEntryPoint()
        self.replaceLabelForIndexInstruction()
        # print(self.executable.lookupTable)
        # print(self.executable.instructions)
        # print(self.executable.entryPoint)

    def process(self):
        processor = Processor()
        system = System(self.executable, processor)
        system.process()

    def replaceLabelForIndexInstruction(self):
        for indexInstruction in self.instructionsToReplace:
            instruction = self.executable.getInstruction(indexInstruction)
            label = instruction.getParameter()
            if label in self.executable.getLookupTable():
                lookupIndex = self.executable.getToLookupTable(label)
                instruction.setParameter(lookupIndex)
            # si no largar un error.

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