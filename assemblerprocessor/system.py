import random
from processor import *
from process import Process, FINISHED, WAITING


class System:

    @classmethod
    def NewSystem(cls, executables, processor):
        cls.instructionsCounter = 0
        cls.burstOfInstructions = 5
        cls.executables = executables
        cls.processor = processor
        cls.processes = [Process(executable) for executable in cls.executables]
        cls.activeProcess = cls.processes[0]  # Validar que no sea nulo
        cls.processor.setProcess(cls.activeProcess)
        cls.active = True

    @classmethod
    def ClockHandler(cls):
        cls.instructionsCounter += 1
        if cls.instructionsCounter >= cls.burstOfInstructions or cls.activeProcess.getState() == FINISHED: 
            cls.processor.saveContext()
            cls.activeProcess = cls.getNextProcess()
            if cls.activeProcess:
                cls.processor.setProcess(cls.activeProcess)
                cls.instructionsCounter = 0    

    @classmethod
    def getNextProcess(cls):
        processes = list(filter(lambda process: (process.getState() == WAITING), cls.processes))
        if len(processes) != 0:
            randomNumber = random.randint(0, len(processes) - 1)
            return processes[randomNumber]
        else:
            cls.active = False
            return None


