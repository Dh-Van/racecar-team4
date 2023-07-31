import sys
sys.path.insert(0, "../../../library")
sys.path.insert(0, "..utils")
import constants, sensor_utils, math_utils
from states import States
import racecar_core, racecar_utils as rc_utils
from typing import Tuple

class lane_follow:

    rc = None

    def __init__(self, racecar: racecar_core.Racecar) -> None:
        self.rc = racecar

    def start(self):
        pass

    def update(self) -> States:
        image = self.rc.camera.get_color_image()
        left_cropped_image = rc_utils.crop(image, constants.LAF_LEFT_IMG_CROP[0], constants.LAF_LEFT_IMG_CROP[1])
        right_cropped_image = rc_utils.crop(image, constants.LAF_RIGHT_IMG_CROP[0], constants.LAF_RIGHT_IMG_CROP[1])

        speed, angle = self.lane_follow(left_cropped_image, right_cropped_image)
        self.rc.drive.set_speed_angle(speed, angle)
        return States.Lane_Follow

    def lane_follow(self, left_image, right_image):
        left_contour, left_contour_center, left_contour_area = sensor_utils.find_contour(
            constants.BLUE_LINE, 
            left_image, 
            50
        )

        right_contour, cropped_right_contour_center, right_contour_area = sensor_utils.find_contour(
            constants.BLUE_LINE, 
            right_image, 
            50
        )

        if(left_contour is None and right_contour is not None):
            print("Not seeing left, seeing right")
            return constants.LF_SPEED, -0.25
        if(left_contour is not None and right_contour is None):
            print("Seeing left, not seeing right")
            return constants.LF_SPEED, 0.25
        if(left_contour is None and right_contour is None):
            print("Not seeing any contours")
            return constants.SAFE_SPEED, 0
        
        print("Seeing both contours")

        right_contour_center = (cropped_right_contour_center, 160 + cropped_right_contour_center[1])
        midpoint = (left_contour_center[1] + right_contour_center[1]) / 2

        angle = self.get_controller_output(midpoint)
        return constants.LF_SPEED, angle


    """
    Function to get the output of a simple P controller. Requires a paramater that is the current
    position of the center of the contour. It uses the constants.WIDTH variable to determine the
    center of the screen. Outputs an angle value between [-1, 1] to be used to steer the racecar
    """
    def get_controller_output(self, center: float) -> float:
        error = center - (constants.WIDTH / 2)
        # if(abs(error) < 25): return 0
        output_px = constants.LF_kP * error
        output_rc = output_px / (constants.WIDTH / 2)
        return math_utils.clamp(output_rc, -1, 1)


