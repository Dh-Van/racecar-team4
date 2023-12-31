# imports
import sys
from enum import IntEnum

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from nptyping import NDArray

sys.path.insert(1, "../library")
import racecar_core
import racecar_utils as rc_utils

# global variables
global rc, color_queue_timer, color_queue_index

rc = racecar_core.create_racecar()

# HSV Values
BLUE = ((90,50,50), (110,255,255))
RED = ((170,100,100), (10,255,255))
GREEN = ((50,50,50), (80,255,255))
ORANGE = ((0,254,254), (1,255,255))
PURPLE = ((140, 50, 50), (160, 255, 255))

# color_queue:   holds tuples of the current color, + next,
#                will be incremented when next is found
color_queue = ((BLUE, GREEN), (GREEN, RED), (RED, BLUE), (BLUE, ORANGE))
color_queue_index = 0
color_queue_timer = 0

MIN_CONTOUR_AREA = 30
LINE_FOLLOW_IMG_CROP = ((360,0), (480, 640))
CONE_STOP_IMG_CROP = ((0,0), (480, 640))


DEFAULT_SAFE_SPEED = 0.15
LINE_FOLLOWING_SPEED = 1.0

# States class:
class State(IntEnum):
    line_follow = 0
    line_follow_final = 1
    cone_follow = 2
    cone_park = 3

# Initialize current_state
curr_state = State.line_follow

# run-functions
def start():
    rc.drive.set_speed_angle(0, 0)

def update():
    speed, angle = 0, 0

    # State Machine
    if(curr_state == State.line_follow):
        speed, angle = line_follow()
        if color_queue_index == len(color_queue) - 1:
            curr_state = State.line_follow_final
        if check_depth_color(): 
            curr_state = State.line_follow_cone
    elif(curr_state == State.line_follow_final):
        speed, angle = line_follow()
        if check_depth_color():
            curr_state = State.line_follow_cone
    elif(curr_state == State.line_follow_cone):
        center, speed, angle = coneFollow()
        if searchForDepth(switchBetweenColorDepth(center)):
            curr_state = State.stop
    elif(curr_state == State.stop):
        speed, angle = 0, 0
    else:
        speed, angle = 0, 0

    rc.drive.set_speed_angle(speed, angle)

"""
Function for following a line based on the color queue.
This function returns a speed and angle value
"""
def line_follow():
    global color_queue_index, color_queue_timer
    # Initial speed and angle values will be set to safe value
    speed, angle = DEFAULT_SAFE_SPEED, 0

    # Gets info about the current color contour and the next color contour in the color queue
    current_contour_center, current_contour_area = findContoursLine(color_queue[color_queue_index][0], LINE_FOLLOW_IMG_CROP)
    next_contour_center, next_contour_area = findContoursLine(color_queue[color_queue_index][1], LINE_FOLLOW_IMG_CROP)

    # Returns the safe values when the current contour is none
    if(current_contour_center is None):
        return speed, angle

    # If the timer is not 1 and the next contour is found
    if color_queue_timer <= 0 and next_contour_center is not None:
        print("next found")
        # The color_queue_index index is incremented so that we can look for the next color pair
        color_queue_index += 1
        # The timer is set 1, cooldown timer so that the camera doesnt immediatley switch colors
        color_queue_timer = 1
        # The current values are set to the next values
        current_contour_center, current_contour_area = next_contour_center, next_contour_area

    # The angle is returned based off of the x value of the current contour center
    angle = get_controller_output(current_contour_center[1])

    # Decrements the color_queue_timer by the delta time so that we know when 1 second has passed
    if color_queue_timer > 0:
        color_queue_timer -= rc.get_delta_time()

    # The speed is a constant set above, and the angle is returned from the controller
    return LINE_FOLLOWING_SPEED, angle

'''
Function to get information about a contour based off a color
Requires a color (hsv tuple list), and a crop rectangle (list of x, y pairs)
Returns the largest contour center and area
'''
def findContoursLine(color, crop):
    image = rc.camera.get_color_image()
    
    # When the image is not found: None, None is returned
    if image is None:
        print("No Image")
        return None, None
    
    # Crop based off of the crop list
    image = rc_utils.crop(image, crop[0], crop[1])
    
    # Find all contours of given color
    list_contours = rc_utils.find_contours(image, color[0], color[1])


    # Gets the largest contour
    lg_contour = rc_utils.get_largest_contour(list_contours, MIN_CONTOUR_AREA)
 
    # cv.drawContours(image, [lg_contour], 0, (0,255,0), 3)
    # plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    # plt.show()

    # If no contour was found: None, None is returned
    if(lg_contour is None):
        return None, None

    # Gets information about the center and area
    contour_center = rc_utils.get_contour_center(lg_contour)
    contour_area = rc_utils.get_contour_area(lg_contour)

    # Returns the largest contour center and area
    return contour_center, contour_area

'''
takes in desired contour center x-value (in pixels),
and outputs new turn angle to correct error
'''
def get_controller_output(center):
    kP = 7
    return clamp(kP * (((center * (2 / 680))) - 1), -1, 1)

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
#Clamps the input

def show_image(image: NDArray) -> None:
    """
    Displays a color image in the Jupyter Notebook.
    """
    img = rc.camera.get_color_image()
    plt.show(img)
def switchBetweenColorDepth(center):
    newCoords = (int(center[0]/2), int(center[1]/2))
    return newCoords
    #320,240
    #160,120

def searchForDepth(center):
    #creates the depth image
    depth_image = rc.camera.get_depth_image()

    #gets the distance of the center pixel within the depth image (we will assume it is off a cone)
    center_distance = depth_image[center[0]][center[1]]

    #checks if the center distance is under 30
    if center_distance < 4:
        return True
    else:
        return False
    
    '''
    Gets the distance of the center pixel, and if it is under an x amount of cm then it is set to true
    '''
def check_depth_color():
    center, area = findContoursLine(PURPLE, CONE_STOP_IMG_CROP)

    if area is not None and area > 3000:
        return True

    '''
    Check the color of the center pixel of the image, once the pixel is seen that it is within the range (HSV)
    '''
    
    
# DO NOT MODIFY: Register start and update and begin execution
if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()

