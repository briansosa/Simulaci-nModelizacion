class Executable:
    def __init__(self):
        self.entryPoint = 0
        self.instructions = []
        self.lookupTable = dict()
        self.sourceCode = []
        self.stack = []

    def getStack(self):
        return self.stack

    def setSourceCode(self, sourceCode):
        self.sourceCode = sourceCode

    def getSourceCode(self):
        return self.sourceCode

    def getLookupTable(self):
        return self.lookupTable

    def getToLookupTable(self, key):
        return self.lookupTable[key]

    def addToLookupTable(self, key, value):
        self.lookupTable[key] = value
    
    def addToInstructions(self, value):
        self.instructions.append(value)

    def getInstructions(self):
        return self.instructions

    def getInstruction(self, key):
        return self.instructions[key]

    def setEntryPoint(self):
        self.entryPoint = self.lookupTable.get("entry_point", 0)

    def getEntryPoint(self):
        return self.entryPoint
