from enum import Enum

class States(Enum):
    Stop = 0
    Line_Follow = 1
    Lane_Follow = 2
    Wall_Follow = 3
    Avoid = 4