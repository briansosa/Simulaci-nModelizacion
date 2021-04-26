from abc import ABC, abstractmethod
from processor import *

class Instruccion(ABC):    
    @abstractmethod
    def processInstruction(self, processor):
        pass

class Mov(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def processInstruction(self, processor):
        if self.param2.isnumeric():
            processor.setRegister(self.param1, int(self.param2))
        else:
            valueRegisterParam2 = processor.getRegister(self.param2)
            processor.setRegister(self.param1, valueRegisterParam2)
        processor.increaseIP()

class Add(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def processInstruction(self, processor):
        valueRegisterParam1 = processor.getRegister(self.param1)
        if self.param2.isnumeric():
            sum = valueRegisterParam1 + self.param2
        else:
            valueRegisterParam2 = processor.getRegister(self.param2)
            sum = valueRegisterParam1 + valueRegisterParam2
        processor.setRegister(self.param1, sum)
        processor.increaseIP()

class Cmp(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def processInstruction(self, processor):
        valueRegisterParam1 = processor.getRegister(self.param1)
        if self.param2.isnumeric():
            if valueRegisterParam1 <= int(self.param2):
                processor.setRegister(FLAG, 1)
            else:
                processor.setRegister(FLAG, 0)
        else:
            valueRegisterParam2 = processor.getRegister(self.param2)
            if valueRegisterParam1 <= valueRegisterParam2:
                processor.setRegister(FLAG, 1)
            else:
                processor.setRegister(FLAG, 0)
        processor.increaseIP()


class Jmp(Instruccion):
    def __init__(self, param):
        self.param = param

    def getParameter(self):
        return self.param

    def setParameter(self, value):
        self.param = value

    def processInstruction(self, processor):
        processor.setRegister(IP, self.param)

class Jnz(Instruccion):
    def __init__(self, param):
        self.param = param

    def getParameter(self):
        return self.param

    def setParameter(self, value):
        self.param = value

    def processInstruction(self, processor):
        if processor.getRegister(FLAG):
            processor.setRegister(IP, self.param)
        else:
            processor.increaseIP()

class Inc(Instruccion):
    def __init__(self, param):
        self.param = param

    def processInstruction(self, processor):
        valueRegister = processor.getRegister(self.param)
        processor.setRegister(self.param, valueRegister + 1)
        processor.increaseIP()
        

class Dec(Instruccion):
    def __init__(self, param):
        self.param = param

    def processInstruction(self, processor):
        valueRegister = processor.getRegister(self.param)
        processor.setRegister(self.param, valueRegister - 1)
        processor.increaseIP()
