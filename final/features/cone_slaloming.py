import sys
sys.path.insert(0, "../../../library")
sys.path.insert(0, "..utils")
import constants, sensor_utils, math_utils
from states import States
import racecar_core, racecar_utils as rc_utils
from typing import Tuple
from enum import Enum

class cone_slalom:

    class States(Enum):
        orange_cone = 0
        purple_cone = 1

    class Cone_States(Enum):
        approach = 0
        avoid = 1
        turn_back = 2

    rc: racecar_core.Racecar = None
    curr_state = States.orange_cone
    cone_state = Cone_States.approach
    colors = [constants.ORANGE_CONE, constants.PURPLE_CONE]

    def __init__(self, racecar) -> None:
        self.rc = racecar

    def start(self): pass

    def update(self):
        if(self.curr_state == self.States.orange_cone):
            self.slalom(self.State.orange_cone)
        if(self.curr_state == self.States.purple_cone):
            self.slalom(self.State.purple_cone)

    def slalom(self, state):
        speed, angle = 0, 0
        color = self.colors[state]

        if(self.curr_state == self.Cone_States.approach):
            speed, angle = self.approach(color)
        if(self.curr_state == self.Cone_States.avoid):
            speed, angle = self.avoid()
        if(self.curr_state == self.Cone_States.turn_back):
            speed, angle = self.turn_back()

        self.rc.drive.set_speed_angle(speed, angle)

        return States.Cone_Slalom

    def approach(self, color):
        image = self.rc.camera.get_color_image()
        cropped_image = rc_utils.crop(image, constants.CS_APPROACH_CROP[0], constants.CS_APPROACH_CROP[1])

        contour, contour_center, contour_area = sensor_utils.find_contour(
            color,
            cropped_image,
            constants.MIN_CONE_AREA
        )

        lidar_window = constants.CS_FORWARD_WINDOW

        scan = self.rc.lidar.get_samples()
        closest = sensor_utils.get_lidar_distances(scan, [lidar_window])[0]

        if closest < 60 and closest > 0:
            self.cone_state = self.Cone_States.avoid
            print("\nAvoid\n")

        if(contour is not None): 
            return constants.CS_FAST_SPEED, self.get_controller_output(contour_center[1])
        
        return constants.CS_FAST_SPEED, 0

    def avoid(self, color):
        speed, angle = 1, constants.CS_AVOID_ANGLE

        lidar_window = constants.CS_FORWARD_WINDOW
        if(color == constants.ORANGE_CONE): 
            lidar_window = constants.CS_LEFT_WINDOW
            angle *= 1
        if(color == constants.PURPLE_CONE): 
            lidar_window = constants.CS_RIGHT_WINDOW
            angle *= -1
    
        scan = self.rc.lidar.get_samples()
        closest = sensor_utils.get_lidar_distances(scan, [lidar_window])[0]

        if (closest < 30 or closest > 99999) and closest > 0:
            print("\nTurnBack\n")   
            self.cone_state = self.Cone_States.turn_back

        return speed, angle

    def turn_back(self, color):
        speed, angle = 1, constants.CS_TURNBACK_ANGLE

        image = self.rc.camera.get_color_image()
        cropped_image = rc_utils.crop(image, constants.CS_SEARCH_CROP[0], constants.CS_SEARCH_CROP[1])

        angle *= 1 if color == constants.ORANGE_CONE else -1

        if(color == constants.ORANGE_CONE): color = constants.PURPLE_CONE
        if(color ==  constants.PURPLE_CONE): color = constants.ORANGE_CONE

        contour, contour_center, contour_area = sensor_utils.find_contour(
            color,
            cropped_image,
            constants.MIN_CONE_AREA
        )

        if(contour is not None):
            self.curr_state = 1 - self.curr_state

        return speed, angle

    def get_controller_output(self, center):
        kP = 0.3
        error = center - (constants.WIDTH / 2)
        output_px = error * kP
        output_rc = output_px / (constants.WIDTH / 2)
        return math_utils.clamp(output_rc, -1, 1)
