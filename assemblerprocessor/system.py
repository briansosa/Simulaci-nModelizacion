import time
from processor import *

SLEEP_SECONDS = 3.5

class System:
    def __init__(self, executable, processor, visualizer):
        self.executable = executable
        self.processor = processor
        self.visualizer = visualizer

    def process(self):
        self.processor.setRegister(IP, self.executable.getEntryPoint())

        instructions = self.executable.getInstructions()
        self.visualizer.showWindow(instructions, self.processor)
        time.sleep(SLEEP_SECONDS)
        while (self.processor.getRegister(IP) < len(instructions)):
            indexInstruction = self.processor.getRegister(IP)
            instruction = instructions[indexInstruction]
            instruction.processInstruction(self.processor)
            self.visualizer.showWindow(instructions, self.processor)
            time.sleep(SLEEP_SECONDS)


