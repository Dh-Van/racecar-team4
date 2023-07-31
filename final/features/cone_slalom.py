import sys
sys.path.insert(0, "../../../library")
sys.path.insert(0, "..utils")
import constants, sensor_utils, math_utils
from states import States
import racecar_core, racecar_utils as rc_utils
from typing import Tuple
from enum import Enum

class cone_slalom:
    class Cone_States(Enum):
        Purple = -1
        Orange = 1

    rc = None
    state = Cone_States.Orange

    def __init__(self, racecar: racecar_core.Racecar) -> None:
        self.rc = racecar

    def start(self):
        pass

    # def update(self):
    #     speed, angle = 

    def approach(self):
        image = self.rc.camera.get_color_image()
        cropped_image = rc_utils.crop(image, (0, 0), (640, 480))
        color = constants.RED_CONE if(self.state == self.Cone_States.Orange) else constants.BLUE_CONE

        # Gets info about the current color contour and the next color contour in the color queue
        current_contour, current_contour_center, current_contour_area = sensor_utils.find_contour(
            color, 
            cropped_image, 
            100
        )

        if(current_contour == None): 
            self.sweep()
            return
        
        


    def sweep(self):
        pass
