AX = "ax"
BX = "bx"
CX = "cx"
DX = "dx"
IP = "ip"
FLAG = "flag"

ACCESIBLE_REGISTERS = [AX, BX, CX, DX]

EMPTY_STACK = "Empty stack. Value not available"

class Processor:
    def __init__(self):
        self.ax = 0
        self.bx = 0
        self.cx = 0
        self.dx = 0
        self.ip = 0
        self.flag = 0
        self.stack = []
    
    def setRegister(self, register, value : int):
        if register == AX:
            self.ax = value
        elif register == BX:
            self.bx = value
        elif register == CX:
            self.cx = value
        elif register == DX:
            self.dx = value
        elif register == IP:
            self.ip = value
        elif register == FLAG:
            self.flag = value
        # ELSE LANZAR UNA EXCEPCION

    def getRegister(self, register):
        if register == AX:
            return self.ax
        elif register == BX:
            return self.bx
        elif register == CX:
            return self.cx
        elif register == DX:
            return self.dx
        elif register == IP:
            return self.ip
        elif register == FLAG:
            return self.flag
        # ELSE LANZAR UNA EXCEPCION

    def pushStack(self, value):
        if not value.isnumeric():
            self.stack.append(self.getRegister(value))
        else:
            self.stack.append(int(value))

    def popStack(self, register : str):
        if len(self.stack) != 0:
            valueStack = self.stack.pop()
            self.setRegister(register, valueStack)
        else:
            raise Exception(EMPTY_STACK)

    def getPopStack(self):
        if len(self.stack) != 0:
            return self.stack.pop()
        else:
            raise Exception(EMPTY_STACK)

        
    def increaseIP(self):
        self.ip += 1

    def showRegisters(self):
        return f"ax: {self.ax}, bx: {self.bx}, cx: {self.cx}, dx: {self.dx}, ip: {self.ip}, flag: {self.flag}, stack: {self.stack}"
            
