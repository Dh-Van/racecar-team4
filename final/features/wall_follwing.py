import sys
sys.path.insert(0, "../../../library")
sys.path.insert(0, "..utils")
import constants, sensor_utils, math_utils
from states import States
import racecar_core, racecar_utils as rc_utils
from typing import Tuple

class wall_follow:

    pid_timer, last_error = 0.001, 0
    rc = None
    wall_distance = 100

    def __init__(self, racecar: racecar_core.Racecar) -> None:
        self.rc = racecar

    def start(self):
        pass

    def update(self):
        speed, angle = self.wall_follow_single(True)
        self.rc.drive.set_speed_angle(speed, angle)
        return States.Wall_Follow
    
    def wall_follow(self) -> Tuple[float, float]:
        speed, angle = 0, 0
        scan = self.rc.lidar.get_samples()
        distances = sensor_utils.get_lidar_distances(scan, constants.WF_WINDOWS)

        right_dist = (distances[1] + distances[2]) / 2
        left_dist = (distances[3] + distances[4]) / 2
        if(right_dist > 9000): right_dist = 20
        if(left_dist > 9000): left_dist = 20
        
        speed = constants.WF_SPEED_SLOW if (distances[0] > constants.WF_FRONT_THRESHOLD) else constants.WF_SPEED_FAST
        if(right_dist > constants.WF_SIDE_THRESHOLD): return speed, 1
        if(left_dist > constants.WF_SIDE_THRESHOLD): return speed, -1

        error = right_dist - left_dist
        angle = self.get_controller_output(error)
        return speed, angle

    def wall_follow_single(self, which_wall) -> Tuple[float, float]:
        speed, angle = 0, 0
        scan = self.rc.lidar.get_samples()
        distances = sensor_utils.get_lidar_distances(scan, constants.WF_WINDOWS)

        right_dist = (distances[1] + distances[2]) / 2
        left_dist = (distances[3] + distances[4]) / 2
        if(right_dist > 9000): right_dist = 20
        if(left_dist > 9000): left_dist = 20
        if(which_wall):
            left_dist = self.wall_distance - right_dist
        else:
            right_dist = self.wall_distance - left_dist
        speed = constants.WF_SPEED_SLOW if (distances[0] > constants.WF_FRONT_THRESHOLD) else constants.WF_SPEED_FAST
        error = right_dist - left_dist
        print(error)
        print(speed, angle)
        angle = self.get_controller_output(error)
        return speed, angle
    
    def get_controller_output(self, error):
        output_ld = constants.WF_kP * error
        return math_utils.clamp(
            math_utils.affine_transformation(
                math_utils.clamp(output_ld, -500, 500), [-500, 500], [-1, 1]
            ), -1, 1
        )