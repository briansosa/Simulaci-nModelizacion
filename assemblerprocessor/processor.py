import time
from system import System
from process import EXECUTING, FINISHED, WAITING
from log import *

AX = "ax"
BX = "bx"
CX = "cx"
DX = "dx"
IP = "ip"
FLAG = "flag"

ACCESIBLE_REGISTERS = [AX, BX, CX, DX]
SLEEP_SECONDS = 0.1
EMPTY_STACK = "Empty stack. Value not available"

class Processor:
    def __init__(self, visualizer):
        self.ax = 0
        self.bx = 0
        self.cx = 0
        self.dx = 0
        self.ip = 0
        self.flag = 0
        self.visualizer = visualizer

    def setProcess(self, process):
        self.process = process
        self.executable = self.process.getExecutable()
        context = self.process.getContext()
        self.ax = context.ax
        self.bx = context.bx
        self.cx = context.cx
        self.dx = context.dx
        self.ip = context.ip
        self.flag = context.flag
        self.process.setState(EXECUTING)

    def saveContext(self):
        context = self.process.getContext()
        context.ax = self.ax
        context.bx = self.bx
        context.cx = self.cx
        context.dx = self.dx
        context.ip = self.ip
        context.flag = self.flag
        if self.process.getState() != FINISHED:
            self.process.setState(WAITING)
    
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
            self.executable.getStack().append(self.getRegister(value))
        else:
            self.executable.getStack().append(int(value))

    def popStack(self, register : str):
        if len(self.executable.getStack()) != 0:
            valueStack = self.executable.getStack().pop()
            self.setRegister(register, valueStack)
        else:
            raise Exception(EMPTY_STACK)

    def getPopStack(self):
        if len(self.executable.getStack()) != 0:
            return self.executable.getStack().pop()
        else:
            raise Exception(EMPTY_STACK)

        
    def increaseIP(self):
        self.ip += 1

    def showRegisters(self):
        return f"ax: {self.ax}, bx: {self.bx}, cx: {self.cx}, dx: {self.dx}, ip: {self.ip}, flag: {self.flag}, stack: {self.executable.getStack()}"
            
    def executeProcess(self):
        while(System.active):
            instructions = self.executable.getInstructions()
            self.visualizer.showWindow(instructions, self)
            time.sleep(SLEEP_SECONDS)
            indexInstruction = self.getRegister(IP)
            instruction = instructions[indexInstruction]
            instruction.processInstruction(self)
            self.visualizer.showWindow(instructions, self)
            time.sleep(SLEEP_SECONDS)
            if self.getRegister(IP) >= len(instructions):
                self.process.setState(FINISHED)
            Log.Write(self.showRegisters())
            System.ClockHandler()
            if self.visualizer.stdscr.getch() == ord('q'):
                raise Exception("Finish program :)")