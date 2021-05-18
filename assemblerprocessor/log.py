class Log:

    @classmethod
    def Init(cls):
        fileLog = open("log.txt", "a")
        fileLog.write("\n")
        fileLog.write("---------------------------------------------------------------\n")
        fileLog.write("\n")
        fileLog.close()

    @classmethod
    def Write(cls, message: str):
        fileLog = open("log.txt", "a")
        fileLog.write(f"{message}\n")
        fileLog.close()
        
    @classmethod
    def WriteLines(cls, messages):
        fileLog = open("log.txt", "a")
        listMessages = list(map(lambda x : str(x) + "\n", messages))
        fileLog.writelines(listMessages)
        fileLog.close()