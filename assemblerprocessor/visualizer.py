from processor import *

class Visualizer:
  def __init__(self, stdscr, height, width):
    self.height = height
    self.width = width
    self.stdscr = stdscr
    self.stdscr.nodelay(True)
    self.stdscr.clear()

  def initWindow(self, instructions, indexEntryPoint):
    # validar el largo con respecto al entry point
    instructionsToShow = instructions[indexEntryPoint: self.height]

    # self.stdscr.addstr(0, 0, 'HOLA')
    # Mostrar los registros en 0
    self.stdscr.addstr(0, 2, "AX")
    self.stdscr.addstr(0, 3, '0')
    self.stdscr.addstr(1, 2, BX)
    self.stdscr.addstr(1, 3, '0')
    self.stdscr.addstr(2, 2, CX)
    self.stdscr.addstr(2, 3, '0')
    self.stdscr.addstr(3, 2, DX)
    self.stdscr.addstr(3, 3, '0')
    self.stdscr.addstr(4, 2, IP)
    self.stdscr.addstr(4, 3, '0')
    self.stdscr.addstr(5, 2, FLAG)
    self.stdscr.addstr(5, 3, '0')

    self.stdscr.refresh()
