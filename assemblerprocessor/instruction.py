from abc import ABC, abstractmethod
from processor import *
from validator import *
import re

MOV = 'mov'
ADD = 'add'
JMP = 'jmp'
JNZ = 'jnz'
CMP = 'cmp'
INC = 'inc'
DEC = 'dec'
PUSH = 'push'
POP = 'pop'
CALL = 'call'
RET = 'ret'

INVALID_PARAMETER = "Parameter: {} is not a valid register"
INVALID_PARAMETER_OR_NUMERIC = "Parameter: {} is not a valid register or is not a numeric value"

VALID_INSTRUCCION = [MOV, ADD, JMP, JNZ, CMP, INC, DEC, PUSH, POP, CALL, RET]

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
        elif self.param2 not in ACCESIBLE_REGISTERS and not Validator.IsNumeric(self.param2):
            raise Exception(INVALID_PARAMETER_OR_NUMERIC.format(self.param2))

    def processInstruction(self, processor):
        if Validator.IsNumeric(self.param2):
            processor.setRegister(self.param1, int(self.param2))
        else:
            valueRegisterParam2 = processor.getRegister(self.param2)
            processor.setRegister(self.param1, valueRegisterParam2)
        processor.increaseIP()

    def toString(self):
        return f"mov {self.param1}, {self.param2}"

class Add(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def validateParameters(self):
        if self.param1 not in ACCESIBLE_REGISTERS:
            raise Exception(INVALID_PARAMETER.format(self.param1))
        elif self.param2 not in ACCESIBLE_REGISTERS and not Validator.IsNumeric(self.param2):
            raise Exception(INVALID_PARAMETER_OR_NUMERIC.format(self.param2))

    def processInstruction(self, processor):
        valueRegisterParam1 = processor.getRegister(self.param1)
        if Validator.IsNumeric(self.param2):
            sum = valueRegisterParam1 + int(self.param2)
        else:
            valueRegisterParam2 = processor.getRegister(self.param2)
            sum = valueRegisterParam1 + valueRegisterParam2
        processor.setRegister(self.param1, sum)
        processor.increaseIP()

    def toString(self):
        return f"add {self.param1}, {self.param2}"

class Cmp(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def validateParameters(self):
        if self.param1 not in ACCESIBLE_REGISTERS and not Validator.IsNumeric(self.param1):
            raise Exception(INVALID_PARAMETER_OR_NUMERIC.format(self.param1))
        elif self.param2 not in ACCESIBLE_REGISTERS and not Validator.IsNumeric(self.param2):
            raise Exception(INVALID_PARAMETER_OR_NUMERIC.format(self.param2))

    def processInstruction(self, processor):
        valueRegisterParam1 = 0
        if Validator.IsNumeric(self.param1):
            valueRegisterParam1 = int(self.param1)
        else:
            valueRegisterParam1 = processor.getRegister(self.param1)
        if Validator.IsNumeric(self.param2):
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

    def toString(self):
        return f"cmp {self.param1}, {self.param2}"

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

    def toString(self):
        return f"jmp {self.param}"

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
    
    def toString(self):
        return f"jnz {self.param}"

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

    def toString(self):
        return f"inc {self.param}"

class Dec(Instruccion):
    def __init__(self, param):
        self.param = param

    def processInstruction(self, processor):
        valueRegister = processor.getRegister(self.param)
        if valueRegister != 0:
            processor.setRegister(self.param, valueRegister - 1)
        processor.increaseIP()

    def validateParameters(self):
        if self.param not in ACCESIBLE_REGISTERS:
            raise Exception(INVALID_PARAMETER.format(self.param))

    def toString(self):
        return f"dec {self.param}"

class Push(Instruccion):
    def __init__(self, param):
        self.param = param

    def processInstruction(self, processor):
        processor.pushStack(self.param)
        processor.increaseIP()

    def validateParameters(self):
        if self.param not in ACCESIBLE_REGISTERS and not Validator.IsNumeric(self.param):
            raise Exception(INVALID_PARAMETER_OR_NUMERIC.format(self.param))

    def toString(self):
        return f"push {self.param}"

class Pop(Instruccion):
    def __init__(self, param):
        self.param = param

    def processInstruction(self, processor):
        processor.popStack(self.param)
        processor.increaseIP()

    def validateParameters(self):
        if self.param not in ACCESIBLE_REGISTERS:
            raise Exception(INVALID_PARAMETER.format(self.param))

    def toString(self):
        return f"pop {self.param}"

class Call(Instruccion):
    def __init__(self, param):
        self.param = param

    def getParameter(self):
        return self.param

    def setParameter(self, value):
        self.param = value

    def processInstruction(self, processor):
        instructionReturn = processor.getRegister(IP) + 1
        processor.pushStack(str(instructionReturn))
        processor.setRegister(IP, self.param)

    def validateParameters(self):
        pass

    def toString(self):
        return f"call {self.param}"

class Ret(Instruccion):
    def processInstruction(self, processor):
        instructionReturn = processor.getPopStack()
        processor.setRegister(IP, instructionReturn)

    def validateParameters(self):
        pass

    def toString(self):
        return "ret"