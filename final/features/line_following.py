import sys, scipy, cv2
sys.path.insert(0, "../../../library")
sys.path.insert(0, "..utils")
from typing import List, Tuple
import constants, math_utils, sensor_utils
from states import States
import racecar_core
import racecar_utils as rc_utils


class line_follow:

    rc = None
    color_queue = []
    color_queue_timer, color_queue_index = 0, 0
    last_contour_center = None

    """
    Initializes the line follower. Requires a racecar object and a list of color pairs
    """
    def __init__(self, racecar: racecar_core.Racecar, color_queue: List[tuple]) -> None:
        self.rc = racecar
        self.color_queue = color_queue

    """
    This function is run once every time the start button is pressed
    """
    def start(self):
        pass

    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    def update(self) -> States:
        speed, angle = self.line_follow()
        self.rc.drive.set_speed_angle(speed, angle)
        if(self.color_queue_index >= len(self.color_queue) - 1):
            return States.Stop
        return States.Line_Follow

    """
    Main line following function. This function uses the color queue passed in earlier
    and changes color as soon as the area of the next color is above a certain value.
    It also goes faster on straights and slower on turns to prevent tipping. It uses
    a simple P controller with gains set in constants. If no image is found or the
    contour color is wrong, then the car will go at a safe speed towards it's last
    angle
    """
    def line_follow(self) -> Tuple[float, float]:
        image = self.rc.camera.get_color_image()
        cropped_image = rc_utils.crop(image, constants.LF_IMG_CROP[0], constants.LF_IMG_CROP[1])

        # Initial speed and angle values will be set to safe value
        speed, angle = constants.SAFE_SPEED, 0

        # Gets info about the current color contour and the next color contour in the color queue
        current_contour, current_contour_center, current_contour_area = sensor_utils.find_contour(
            self.color_queue[self.color_queue_index][0], 
            cropped_image, 
            constants.LF_MIN_CONTOUR_AREA
        )
        next_contour, next_contour_center, next_contour_area = sensor_utils.find_contour(
            self.color_queue[self.color_queue_index][1], 
            cropped_image, 
            constants.LF_MIN_CONTOUR_AREA
        )

        # Changes to the next color pair in the color queue, since the second color has been found
        if self.color_queue_timer <= 0 and next_contour_area > 750:
            print("next color found")
            # The color_queue_index index is incremented so that we can look for the next color pair
            self.color_queue_index += 1
            # The timer is set 1, cooldown timer so that the camera doesnt immediatley switch colors
            self.color_queue_timer = 2
            # The current values are set to the next values since the car is on the next color
            current_contour, current_contour_center, current_contour_area = next_contour, next_contour_center, next_contour_area

        # Returns the safe values if the current contour is none
        if(current_contour_center is None and self.last_contour_center is not None):
            angle = self.get_controller_output(self.last_contour_center[1])
            print("not seen - angle: ", angle)
            return speed, angle

        # The angle is returned based off of the x value of the current contour center
        angle = self.get_controller_output(current_contour_center[1])

        # Decrements the self.color_queue_timer by the delta time so that we know when 1 second has passed
        if self.color_queue_timer > 0:
            self.color_queue_timer -= self.rc.get_delta_time()
        
        if(self.last_contour_center is not None):
            if(abs(self.last_contour_center[1] - current_contour_center[1]) >= 10):
                # angle = self.get_controller_output(self.last_contour_center[1])
                angle = math_utils.clamp(self.last_contour_center[1] * 10, -1, 1)
                self.last_contour_center = current_contour_center
                print("slowed down - angle: ", angle)
                return constants.LF_TURN_SPEED, angle

        # rc_utils.draw_contour(cropped_image, current_contour)
        # self.rc.display.show_color_image(cropped_image)
        # The speed is a constant set in the constants file, and the angle is returned from the controller
        self.last_contour_center = current_contour_center
        print("fast - angle: ", angle)
        return constants.LF_SPEED, angle

    """
    Function to get the output of a simple P controller. Requires a paramater that is the current
    position of the center of the contour. It uses the constants.WIDTH variable to determine the
    center of the screen. Outputs an angle value between [-1, 1] to be used to steer the racecar
    """
    def get_controller_output(self, center: float) -> float:
        error = center - (constants.WIDTH / 2)
        output_px = constants.LF_kP * error
        output_rc = output_px / (constants.WIDTH / 2)
        return math_utils.clamp(output_rc, -1, 1)
