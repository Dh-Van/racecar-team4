from enum import Enum

class States(Enum):
    Stop = 0
    Line_Follow = 1
    Wall_Follow = 2
    Cone_Slalom = 3
    Lane_Follow = 4