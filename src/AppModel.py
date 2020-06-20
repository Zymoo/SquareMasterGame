import random

class AppModel:
    def __init__(self):
        self.counter = 0
        self.position = (0, 0)

    def getNextPosition(self):
        x = random.randrange(8)
        y = random.randrange(8)
        self.position = (x, y)
        return self.position

    def getCurrentPosition(self):
        return self.position

    def getCurrentNotation(self):
        return str(chr(self.position[1] + ord('A'))) + str(str(8 - self.position[0]))

    def counterReset(self):
        self.counter = 0
        self.position = (0, 0)

    def counterAdd(self):
        self.counter += 1

    def getCounter(self):
        return self.counter