import random
from log import *
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
        cls.activeProcess = cls.processes[0]
        cls.processor.setProcess(cls.activeProcess)
        cls.active = True
        Log.WriteLines(["Processes:", cls.processes])
        Log.WriteLines(["Active process:", cls.activeProcess])

    @classmethod
    def ClockHandler(cls):
        cls.instructionsCounter += 1
        if cls.instructionsCounter >= cls.burstOfInstructions or cls.activeProcess.getState() == FINISHED:
            cls.processor.saveContext()
            cls.activeProcess = cls.getNextProcess()
            Log.WriteLines(["Change context. Active process:", cls.activeProcess])
            if cls.activeProcess:
                cls.processor.setProcess(cls.activeProcess)
                cls.instructionsCounter = 0    

    @classmethod
    def getNextProcess(cls):
        index = cls.processes.index(cls.activeProcess)
        waitingProcesses = list(filter(lambda process: (process.getState() == WAITING), cls.processes[index + 1:]))
        if len(waitingProcesses) != 0:
            return waitingProcesses[0]
        else:
            waitingProcesses = list(filter(lambda process: (process.getState() == WAITING), cls.processes[:index]))
            if len(waitingProcesses) != 0:
                return waitingProcesses[0]
            elif cls.activeProcess.getState() == WAITING:
                return cls.activeProcess 
            else:
                cls.active = False
                return None
