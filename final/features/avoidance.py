import sys, scipy, cv2, math
sys.path.insert(0, "../../../library")
sys.path.insert(0, "..utils")
from typing import List, Tuple
import constants, math_utils, sensor_utils
from states import States
from directions import Directions
import racecar_core
import racecar_utils as rc_utils
from enum import Enum

class avoid:

    class avoidance_states(Enum):
        Approach = 0
        Avoid = 1
        Correct = 2

    rc = None
    turn_timer = 0

    def __init__(self, racecar: racecar_core.Racecar) -> None:
        self.rc = racecar


    def update(self):
        scan = self.rc.lidar.get_samples()
        front_dist = sensor_utils.get_lidar_distances(scan, [(-20, 20)])[0]
        if(front_dist < 60):
            self.rc.drive.set_speed_angle(0.15, 1) 
            self.turn_timer += self.rc.get_delta_time()
        elif(self.turn_timer > 0):
            self.rc.drive.set_speed_angle(0.15, -1)
            self.turn_timer -= self.rc.get_delta_time()
        else:
            self.rc.drive.set_speed_angle(0.15, 0)

        return States.Avoid