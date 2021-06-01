from executable import *
from instruction import *
from processor import *
from system import *
import re

COMMENT = "#"
COMPILATION_ERROR = "Error in file {filename} line {line}: {error}"
INVALID_LINE = "Invalid line"
LABEL_NOT_FOUND = "Label '{label}' not found."


class Assembler:
    def __init__(self):
        self.error = ""
        self.executable = Executable()
        self.instructionsToReplace = []
        self.listInstructionLibraries = []
        self.indexInstruction = 0

    def generateExecutable(self, filename):
        with open(filename) as file:
            self.executable.setSourceCode(self.getSourceCodeFromFile(file))

        self.generateInstructionLibraries(self.executable.getSourceCode())
        self.processLibraries()
        self.processSourceCode(filename, self.executable.getSourceCode())

        if not self.error: 
            self.executable.setEntryPoint()
            self.replaceLabelForIndexInstruction()

    def generateInstructionLibraries(self, sourceCode):
        for line in sourceCode:
            if self.isInclude(line):
                fileLibrary = self.getIncludeFile(line)
                with open(fileLibrary) as file:
                    fileListInstructions = self.getSourceCodeFromFile(file)
                    self.generateInstructionLibrariesDetails(fileListInstructions, fileLibrary)

    def generateInstructionLibrariesDetails(self, sourceCode, filename):
        instructionFile = []
        for line in sourceCode:
            if self.isInclude(line):
                fileLibrary = self.getIncludeFile(line)
                with open(fileLibrary) as file:
                    fileListInstructions = self.getSourceCodeFromFile(file)
                    self.generateInstructionLibrariesDetails(fileListInstructions, fileLibrary)
            else:
                instructionFile.append(line)
        self.listInstructionLibraries.append((filename, instructionFile))

    def processLibraries(self):
        for filename, sourceCode in self.listInstructionLibraries:
            self.processSourceCode(filename, sourceCode)

    def processSourceCode(self, filename, sourceCode):
        for indexSourceCode, line in enumerate(sourceCode):
            if len(line) == 0 or line[0] == COMMENT or self.isInclude(line):
                continue
            elif self.isLabel(line):
                label = self.getLabel(line)
                self.executable.addToLookupTable(label, self.indexInstruction)
            elif self.isInstruction(line):
                instructionName, parameters = self.parseInstruction(line)
                try:
                    if not parameters:
                        instruction = self.generateInstructionWithoutParameter(instructionName)
                    else:
                        instruction = self.generateInstruction(instructionName, parameters)
                        instruction.validateParameters()
                    self.executable.addToInstructions(instruction)
                    if isinstance(instruction, Jmp) or isinstance(instruction, Jnz) or isinstance(instruction, Call):
                        self.instructionsToReplace.append([self.indexInstruction, indexSourceCode, filename])
                    self.indexInstruction += 1
                except Exception as e:
                    self.error = COMPILATION_ERROR.format(filename = filename, line = indexSourceCode, error = str(e))
                    break
            else:
                self.error = COMPILATION_ERROR.format(filename = filename, line = indexSourceCode, error = INVALID_LINE)

    def hasError(self):
        return self.error != ""

    def getError(self):
        return self.error

    def replaceLabelForIndexInstruction(self):
        for instructionToReplace in self.instructionsToReplace:
            indexInstruction, indexSourceCode, filename = instructionToReplace[0], instructionToReplace[1], instructionToReplace[2]
            instruction = self.executable.getInstruction(indexInstruction)
            label = instruction.getParameter()
            if label in self.executable.getLookupTable():
                lookupIndex = self.executable.getToLookupTable(label)
                instruction.setParameter(lookupIndex)
            else:
                self.error = COMPILATION_ERROR.format(filename = filename, line = indexSourceCode, error = LABEL_NOT_FOUND.format(label = label)) 

    def generateInstruction(self, instructionName, parameters):
        listParams = self.parseParameters(parameters)
        if len(listParams) == 1:
            if instructionName == JMP:
                return Jmp(listParams[0])
            elif instructionName == JNZ:
                return Jnz(listParams[0])
            elif instructionName == INC:
                return Inc(listParams[0])
            elif instructionName == DEC:
                return Dec(listParams[0])
            elif instructionName == PUSH:
                return Push(listParams[0])
            elif instructionName == POP:
                return Pop(listParams[0])
            elif instructionName == CALL:
                return Call(listParams[0])
        elif len(listParams) == 2:
            if instructionName == MOV:
                return Mov(listParams[0], listParams[1])
            elif instructionName == ADD:
                return Add(listParams[0], listParams[1])
            elif instructionName == CMP:
                return Cmp(listParams[0], listParams[1])
        else:
            raise Exception("Error to generate instruction")

    def generateInstructionWithoutParameter(self, instructionName):
        if instructionName == RET:
            return Ret()  
        else:
            raise Exception("Error to generate instruction")


    def parseParameters(self, parameters):
        parametersList = []
        oneParamRegex = '^([\w\-]+)\s*$'
        twoParamRegex = '^([\w\-]+)\s*,\s*([\w\-]+)\s*$'
        oneParamMatch = re.search(oneParamRegex, parameters)
        if oneParamMatch:
            parametersList.append(oneParamMatch.group(1))
        else:
            twoParamMatch = re.search(twoParamRegex, parameters)
            if twoParamMatch:
                parametersList.append(twoParamMatch.group(1))
                parametersList.append(twoParamMatch.group(2))
            else:
                raise Exception("Invalid parameters")

        return parametersList

    def isLabel(self, line):
        match = re.search('^([\w_]+):$', line)
        return match

    def getLabel(self, line):
        match = re.search('^([\w_]+):$', line)
        return match.group(1)

    def isInclude(self, line):
        match = re.search('^include\s+([\w]*.asm)$', line)
        return match

    def getIncludeFile(self, line):
        match = re.search('^include\s+([\w]*.asm)$', line)
        return match.group(1)

    def isInstruction(self, line):
        match = re.search('^(ret)', line)
        if match:
            return match and match.group(1) in VALID_INSTRUCCION
        match = re.search('^(mov|add|cmp|inc|dec|jmp|jnz|push|pop|call)\s+([\w_\-,\s]+)', line)
        return match and match.group(1) in VALID_INSTRUCCION
    
    def parseInstruction(self, line):
        if re.search('^(ret)', line):
            return ("ret","")
        match = re.search('^(mov|add|cmp|inc|dec|jmp|jnz|push|pop|call)\s+([\w_,\-\s]+)', line)
        return (match.group(1), match.group(2))

    def cleanLine(self, line):
        line = line.strip()
        line = line.replace('\t', '')
        line = line.replace('\n', '')
        line = line.lower()
        return line    

    def getExecutable(self):
        return self.executable

    def getSourceCodeFromFile(self, file):
        listCleanLines = [self.cleanLine(line) for line in file if len(self.cleanLine(line)) != 0 and self.cleanLine(line)[0] != COMMENT]
        return listCleanLines

    def clear(self):
        self.error = ""
        self.executable = Executable()
        self.instructionsToReplace = []
        self.listInstructionLibraries = []
        self.indexInstruction = 0