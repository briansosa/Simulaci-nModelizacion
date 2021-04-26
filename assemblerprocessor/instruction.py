from abc import ABC, abstractmethod
from processor import *
import re

MOV = 'mov'
ADD = 'add'
JMP = 'jmp'
JNZ = 'jnz'
CMP = 'cmp'
INC = 'inc'
DEC = 'dec'

INVALID_PARAMETER = "Parameter: {} is not a valid register"
INVALID_PARAMETER_OR_NUMERIC = "Parameter: {} is not a valid register or is not a numeric value"

VALID_INSTRUCCION = [MOV, ADD, JMP, JNZ, CMP, INC, DEC]

class Instruccion(ABC):    
    @abstractmethod
    def processInstruction(self, processor):
        pass

    @abstractmethod
    def validateParameters(self):
        pass

class Mov(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def validateParameters(self):
        if self.param1 not in ACCESIBLE_REGISTERS:
            raise Exception(INVALID_PARAMETER.format(self.param1))
        elif self.param2 not in ACCESIBLE_REGISTERS and not self.param2.isnumeric():
            raise Exception(INVALID_PARAMETER_OR_NUMERIC.format(self.param2))

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

    def validateParameters(self):
        if self.param1 not in ACCESIBLE_REGISTERS:
            raise Exception(INVALID_PARAMETER.format(self.param1))
        elif self.param2 not in ACCESIBLE_REGISTERS and not self.param2.isnumeric():
            raise Exception(INVALID_PARAMETER_OR_NUMERIC.format(self.param2))

    def processInstruction(self, processor):
        valueRegisterParam1 = processor.getRegister(self.param1)
        if self.param2.isnumeric():
            sum = valueRegisterParam1 + int(self.param2)
        else:
            valueRegisterParam2 = processor.getRegister(self.param2)
            sum = valueRegisterParam1 + valueRegisterParam2
        processor.setRegister(self.param1, sum)
        processor.increaseIP()

class Cmp(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def validateParameters(self):
        if self.param1 not in ACCESIBLE_REGISTERS:
            raise Exception(INVALID_PARAMETER.format(self.param1))
        elif self.param2 not in ACCESIBLE_REGISTERS and not self.param2.isnumeric():
            raise Exception(INVALID_PARAMETER_OR_NUMERIC.format(self.param2))

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

    def validateParameters(self):
        pass

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

    def validateParameters(self):
        pass
    

class Inc(Instruccion):
    def __init__(self, param):
        self.param = param

    def processInstruction(self, processor):
        valueRegister = processor.getRegister(self.param)
        processor.setRegister(self.param, valueRegister + 1)
        processor.increaseIP()
        
    def validateParameters(self):
        if self.param not in ACCESIBLE_REGISTERS:
            raise Exception(INVALID_PARAMETER.format(self.param))

class Dec(Instruccion):
    def __init__(self, param):
        self.param = param

    def processInstruction(self, processor):
        valueRegister = processor.getRegister(self.param)
        processor.setRegister(self.param, valueRegister - 1)
        processor.increaseIP()

    def validateParameters(self):
        if self.param not in ACCESIBLE_REGISTERS:
            raise Exception(INVALID_PARAMETER.format(self.param))