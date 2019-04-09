import turtle
import random

MAX_X = 2560
MAX_Y = 1440
MAX_DROPS = 100

class Rain():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(1, 5)
