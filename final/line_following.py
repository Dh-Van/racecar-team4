import sys, scipy
import constants, math_utils, camera_utils
sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils


class line_follow:

    rc = None
    color_queue = []
    color_queue_timer, color_queue_index = 0, 0

    def __init__(self, racecar: racecar_core.Racecar, color_queue) -> None:
        self.rc = racecar
        self.color_queue = color_queue

    def start(self):
        pass

    def update(self):
        speed, angle = self.line_follow()
        print(angle)
        self.rc.drive.set_speed_angle(speed, angle)

    def line_follow(self):
        image = self.rc.camera.get_color_image()
        cropped_image = rc_utils.crop(image, constants.LF_IMG_CROP_SIM[0], constants.LF_IMG_CROP_SIM[1])

        # Initial speed and angle values will be set to safe value
        speed, angle = constants.SAFE_SPEED, 0

        # Gets info about the current color contour and the next color contour in the color queue
        contour, current_contour_center, current_contour_area = camera_utils.find_contours(self.color_queue[self.color_queue_index][0], cropped_image, 30)
        n_contour, next_contour_center, next_contour_area = camera_utils.find_contours(self.color_queue[self.color_queue_index][1], cropped_image, 30)


        rc_utils.draw_contour(cropped_image, contour)
        rc_utils.draw_circle(cropped_image, current_contour_center)
        
        self.rc.display.show_color_image(cropped_image)

        # Returns the safe values when the current contour is none
        if(current_contour_center is None):
            return speed, angle

        # If the timer is not 1 and the next contour is found
        if self.color_queue_timer <= 0 and next_contour_area > 2000:
            print("next found")
            # The color_queue_index index is incremented so that we can look for the next color pair
            self.color_queue_index += 1
            # The timer is set 1, cooldown timer so that the camera doesnt immediatley switch colors
            self.color_queue_timer = 2
            # The current values are set to the next values
            current_contour_center, current_contour_area = next_contour_center, next_contour_area

        # The angle is returned based off of the x value of the current contour center
        angle = self.get_controller_output(current_contour_center[1])

        # Decrements the self.color_queue_timer by the delta time so that we know when 1 second has passed
        if self.color_queue_timer > 0:
            self.color_queue_timer -= self.rc.get_delta_time()
            
        faster_crop = rc_utils.crop(image, constants.LF_STRAIGHT_IMG_CROP[0], constants.LF_STRAIGHT_IMG_CROP[1])
        # Checks if car is on long straight-away, and returns faster speed
        l_contour, long_contour_center, long_contour_area = camera_utils.find_contours(self.color_queue[self.color_queue_index][0], cropped_image, False)
        if long_contour_area > 1000:
            return constants.LF_STRAIGHT_SPEED, angle
        # The speed is a constant set above, and the angle is returned from the controller
        return constants.LF_SPEED, angle



    def get_controller_output(self, center):
        error = center - (constants.WIDTH / 2)
        # curr_time = self.rc.get_delta_time()
        # slope = (error - self.error_list[-1]) / (curr_time - self.time_list[-1])
        # integral_sum = scipy.integrate.simps(self.error_list, self.time_list)
        # output_px = (constants.LINE_FOLLOW_kP * (error) + (constants.LINE_FOLLOW_kI * integral_sum) + (constants.LINE_FOLLOW_kD * slope))
        output_px = constants.LF_kP * error

        output_rc = output_px / (constants.WIDTH / 2)

        # self.error_list.append(error)
        # self.time_list.append(curr_time)
        return math_utils.clamp(output_rc, -1, 1)
