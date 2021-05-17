EXECUTING = 'executing'
FINISHED = 'finished'
WAITING = 'waiting'

class Process:
    def __init__(self, executable):
        self.executable = executable
        self.context = Context()
        self.context.ip = self.executable.getEntryPoint()
        self.state = WAITING

    def getExecutable(self):
        return self.executable

    def getContext(self):
        return self.context
    
    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

class Context:
    def __init__(self):
        self.ax = 0
        self.bx = 0
        self.cx = 0
        self.dx = 0
        self.ip = 0
        self.flag = 0