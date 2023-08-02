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
    turn_dist = 100
    front_weight = 0.7
    side_weight = 0.3

    def __init__(self, racecar: racecar_core.Racecar) -> None:
        self.rc = racecar

    def start(self):
        pass

    def update(self):
#         speed, angle = self.wall_follow_single(True)
        speed, angle = self.wall_follow()
        angle = math_utils.clamp(angle, -1, 1)
        self.rc.drive.set_speed_angle(speed, angle)
        return States.Wall_Follow
    
    def wall_follow(self) -> Tuple[float, float]:
        speed, angle = constants.WF_SPEED_FAST, 0
        scan = self.rc.lidar.get_samples()
        distances = sensor_utils.get_lidar_distances(scan, constants.WF_WINDOWS)
        front_dist = distances[0]
        right_dist = (distances[1] + distances[2]) / 2
        left_dist = (distances[3] + distances[4]) / 2
        
        if(right_dist > 9000): right_dist = 20
        if(left_dist > 9000): left_dist = 20
        if(front_dist > 9000): front_dist = 20
        
        if(front_dist <= 200):
            angle_multiplier = 0.15
            if(distances[3] > distances[1]): angle_multiplier *= -1
                
            angle = (100 / front_dist) * angle_multiplier
            print("Very Close",  front_dist, angle)
            return constants.WF_SPEED_SLOW, angle
        
        print("Not Close", front_dist, angle)
                 
        if(right_dist > constants.WF_SIDE_THRESHOLD): return speed, 1
        if(left_dist > constants.WF_SIDE_THRESHOLD): return speed, -1

        error = right_dist - left_dist
        angle = self.get_controller_output(error)
        return speed, angle

    def wall_follow_single(self) -> Tuple[float, float]:
        speed, angle = constants.WF_SPEED_FAST, 0
        scan = self.rc.lidar.get_samples()
        distances = sensor_utils.get_lidar_distances(scan, constants.WF_WINDOWS)
        front_dist = distances[0]
        right_dist = (distances[1] + distances[2]) / 2
        left_dist = self.wall_distance - right_dist
        
        if(right_dist > 9000): right_dist = 20
        if(left_dist > 9000): left_dist = 20
        if(front_dist > 9000): front_dist = 20
        
        if(front_dist <= 200):
            angle_multiplier = -0.15
                
            angle = (100 / front_dist) * angle_multiplier
            print("Very Close",  front_dist, angle)
            return constants.WF_SPEED_SLOW, angle
        
        print("Not Close", front_dist, angle)
                
        if(right_dist > 99): return speed, 1

        error = right_dist - left_dist
        angle = self.get_controller_output(error)
        return speed, angle
    
    def get_controller_output(self, error):
        output_ld = constants.WF_kP * error
        return math_utils.clamp(
            math_utils.affine_transformation(
                math_utils.clamp(output_ld, -200, 200), [-200, 200], [-0.25, 0.25]
            ), -1, 1
        )