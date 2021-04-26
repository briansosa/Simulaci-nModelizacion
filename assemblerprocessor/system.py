from processor import *

class System:
    def __init__(self, executable, processor):
        self.executable = executable
        self.processor = processor

    def process(self):
        self.processor.setRegister(IP, self.executable.getEntryPoint())
        # print(self.processor.ip)

        instructions = self.executable.getInstructions()
        while (self.processor.getRegister(IP) < len(instructions)):
            indexInstruction = self.processor.getRegister(IP)
            instruction = instructions[indexInstruction]
            instruction.processInstruction(self.processor)
            print(self.processor.showRegisters())
            # print(self.processor.getRegister(IP))

