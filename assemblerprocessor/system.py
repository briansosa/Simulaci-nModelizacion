from processor import *

class System:
    def __init__(self, executable, processor, visualizer):
        self.executable = executable
        self.processor = processor
        self.visualizer = visualizer

    def process(self):
        self.processor.setRegister(IP, self.executable.getEntryPoint())

        instructions = self.executable.getInstructions()
        self.visualizer.initWindow(instructions,self.processor.getRegister(IP))
        # print(self.processor.ip)

        while (self.processor.getRegister(IP) < len(instructions)):
            indexInstruction = self.processor.getRegister(IP)
            instruction = instructions[indexInstruction]
            instruction.processInstruction(self.processor)
            #print(self.processor.showRegisters())

            # Visualizer: UpdatePointer(indexInstruction)

