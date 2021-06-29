from processor import *
import curses
import math

ARROW = "->"
NOT_ARROW = "  "
SEPARATOR = "|"

class Visualizer:
  def __init__(self, stdscr, height, width):
    if height > 10:
      raise Exception("Max height in visualizer is 10")
    self.height = height
    self.width = width
    self.stdscr = stdscr
    self.stdscr.nodelay(True)
    self.stdscr.clear()
    self.arrowIndex = 1
    self.instructionIndex = 6
    self.registerIndex = 22
    self.registerValueIndex = 29

  def showWindow(self, instructions, processor):
    self.stdscr.clear()
    instructionPointer = processor.getRegister(IP)
    self.instructions = instructions

    indexArrow = 0
    listToShow = []
    if instructionPointer <= math.floor(self.height/2):
        previousList = instructions[:instructionPointer]
        listToShow = instructions[instructionPointer-len(previousList):self.height]
        indexArrow = instructionPointer
    else:
        middleHeight = self.height/2
        fromIndex = instructionPointer - math.floor(middleHeight)
        toIndex = instructionPointer + math.floor(middleHeight)
        if (self.height%2) != 0:
            listToShow = instructions[fromIndex - 1: toIndex]
        else:
            listToShow = instructions[fromIndex: toIndex]
        indexArrow = math.floor(middleHeight)
      
    self.buildWindow(listToShow, processor, indexArrow)
    self.stdscr.refresh()

  def buildWindow(self, instructions, processor, indexArrow):
    lenInstructions = max(len(instructions), 6)
    for index in range(0, lenInstructions):
      stringInstruction = ""
      if len(instructions) > index:
          instruction = instructions[index]
          stringInstruction = instruction.toString()
      if index == 0:
        line = self.buildLine(index == indexArrow, stringInstruction, True, (AX, processor.getRegister(AX)))
      elif index == 1:
        line = self.buildLine(index == indexArrow, stringInstruction, True, (BX, processor.getRegister(BX)))
      elif index == 2:
        line = self.buildLine(index == indexArrow, stringInstruction, True, (CX, processor.getRegister(CX)))
      elif index == 3:
        line = self.buildLine(index == indexArrow, stringInstruction, True, (DX, processor.getRegister(DX)))
      elif index == 4:
        line = self.buildLine(index == indexArrow, stringInstruction, True, (IP, processor.getRegister(IP)))
      elif index == 5:
        line = self.buildLine(index == indexArrow, stringInstruction, True, (FLAG, processor.getRegister(FLAG)))
      else:
        line = self.buildLine(index == indexArrow, stringInstruction, False)
      self.stdscr.addstr(index, 0, line)


  def buildLine(self, hasArrow, instruction, hasRegister, register = ()):
    line = " " * self.width
    if hasArrow:
      line = self.replaceStrIndex(line, self.arrowIndex, ARROW)
    else:
      line = self.replaceStrIndex(line, self.arrowIndex, NOT_ARROW)
    line = self.replaceStrIndex(line, self.arrowIndex + len(ARROW) + 1, SEPARATOR)
    line = self.replaceStrIndex(line, self.instructionIndex, instruction)
    if hasRegister:
      line = self.replaceStrIndex(line, self.registerIndex - 2, SEPARATOR)
      line = self.replaceStrIndex(line, self.registerIndex, register[0].center(4))
      line = self.replaceStrIndex(line, self.registerIndex + len(register[0].center(4)) + 1, SEPARATOR)
      line = self.replaceStrIndex(line, self.registerValueIndex, register[1])
    return line

  def replaceStrIndex(self, text, index=0, replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])
