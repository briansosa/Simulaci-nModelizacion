import math

def main():
    for i in range(0, 13):
        pepe(i)


def pepe(heightt):
    instructions = ["a","b","c","d","e","f","g","h","i","j","k","l"]
    height = heightt
    instructionPointer = 12
    indexArrow = 0
    listToShow = []
    if instructionPointer <= math.floor(height/2):
        previousList = instructions[:instructionPointer]
        listToShow = instructions[instructionPointer-len(previousList):height]
        indexArrow = instructionPointer
    else:
        middleHeight = height/2
        fromIndex = instructionPointer - math.floor(middleHeight)
        toIndex = instructionPointer + math.floor(middleHeight)
        if (height%2) != 0:
            listToShow = instructions[fromIndex - 1: toIndex]
        else:
            listToShow = instructions[fromIndex: toIndex]
        indexArrow = math.floor(middleHeight)
    print(listToShow)

main()
