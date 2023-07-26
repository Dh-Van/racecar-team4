# imports
import sys
from enum import IntEnum

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from nptyping import NDArray
import math

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

# global variables
global rc


rc = racecar_core.create_racecar()

# HSV Values
BLUE = ((90,70,70), (110,255,255))
RED = ((170,100,100), (10,255,255))

WIDTH = 640
HEIGHT = 480


MIN_CONTOUR_AREA = 1

# States class:
class State(IntEnum):
    red_cone = 0
    blue_cone = 1

class ConeState(IntEnum):
    approach = 0
    avoid = 1
    turnBack = 2
    align = 3
# Initialize current_state
curr_state = State.red_cone
cone_state = ConeState.approach

# run-functions
def start():
    rc.drive.set_speed_angle(0, 0)

def update():
    # State Machine
    if(curr_state == State.red_cone):
        Slalom([RED, BLUE], turn = 1)
    elif(curr_state == State.blue_cone):
        Slalom([BLUE, RED], turn = -1) # Left
    else:
        speed, angle = 0, 0
        rc.drive.set_speed_angle(speed, angle)

'''
Main function that runs when cone slalom is entered.
Runs once for each cone, with the color determining direction or bool Right.
Drives around the cone and changes the state according to which color the next one is.
'''
def Slalom(colors, turn = 1):
    global cone_state, curr_state

    # When Color camera detects Cone (Color Camera) -> Approach the cone
    if cone_state == ConeState.approach:
        center = findCone(colors[1])
        if center == None:
            rc.drive.set_speed_angle(0.5, 0)
        else:
            rc.drive.set_speed_angle(0.5, get_controller_output(center[1]))
        # When car reaches a given distance from cone (LIDAR) -> Turn wheels right + drive straight
        d = LidarCone((680, 40))[1]
        print(d)
        if d <= 90 and d > 0:
            print('avoid')
            cone_state = ConeState.avoid

    # -> Turn wheels + avoid cone
    if cone_state == ConeState.avoid:
        if turn == -1:
            rc.drive.set_speed_angle(0.3, 0.35 * turn)
            # When cone reaches ~90° from car (LIDAR) -> Turn back to the left
            d = LidarCone((100, 180))[1]
            if d <= 50 and d > 0:
                print('turn back')
                cone_state = ConeState.turnBack
        else:
            rc.drive.set_speed_angle(0.3, 0.35 * turn)
            # When cone reaches ~90° from car (LIDAR) -> Turn back to the right
            d = LidarCone((520, 600))[1]
            if d <= 50 and d > 0:
                print('turn back')
                cone_state = ConeState.turnBack
    # -> Turn back to the center

    if cone_state == ConeState.turnBack:
        rc.drive.set_speed_angle(0.3, 1 * turn * -1)
        # When car is between cones (LIDAR) -> Drive towards next cone
        front = LidarCone((640, 120))
        back_angle = int(front[0] + 360) % 720
        back = LidarCone((back_angle - 40, back_angle + 40))
        if front[1] > 0 and back[1] > 0:
            if front[1] <= 500 and back[1] <= 100:
                print('align')
                print(front[0], back[0])
                cone_state = ConeState.align
                rc.drive.set_speed_angle(0.3, 1 * turn)

    # -> Drive towards next cone
    if cone_state == ConeState.align:
        center = findCone(colors[-1])
        if center == None:
            pass
        else:
            rc.drive.set_speed_angle(0.3, get_controller_output(center[1]))
        # When car reaches a given distance from cone (LIDAR) -> Turn wheels right + drive straight
            d = LidarCone((680, 40))[1]
            if d <= 200 and d > 0:
                print('next')
                print('approach')
                cone_state = ConeState.approach
                if curr_state == State.red_cone:
                    curr_state = State.blue_cone
                elif curr_state == State.blue_cone:
                    curr_state = State.red_cone

    # Detect color of cone + change state to red / blue [TODO]



'''
Finds the nearest cone using the LIDAR data
Returns the angle and distance
'''
def LidarCone(window = (710, 10)):
    scan = rc.lidar.get_samples_async()
    lower = window[0]
    upper = window[1]
    x = 0
    if lower > upper:
        x = 720
    distances = []
    angles = []
    for i in range(lower - x, upper):
        if scan[i] > 0 and scan[i] < 200:
            distances.append(scan[i])

            angles.append((i + x) % 720)

    if len(angles) == 0:
        return 0, 0
    return sum(angles) / len(angles), sum(distances) / len(distances)


'''
Detects a cone with a given color.
Will only be triggered if cone is the closest cone, also in FOV
'''
def findCone(color):
    image = rc.camera.get_color_image()
    
    # When the image is not found: None, None is returned
    if image is None:
        print("No Image")
        return None
    
    cropped_image = rc_utils.crop(image, (200, 0), (480, 640))
    # Find all contours of given color
    list_contours = rc_utils.find_contours(cropped_image, color[0], color[1])

    # Gets the largest contour
    lg_contour = rc_utils.get_largest_contour(list_contours, MIN_CONTOUR_AREA)
 
    # If no contour was found: None, None is returned
    if(lg_contour is None):
        print("No Contour")
        return None

    # # Returns the largest contour center
    # print(lg_contour)
    return rc_utils.get_contour_center(lg_contour) 


def get_controller_output(center):
    kP = 1
    return clamp(kP * (((center / WIDTH) * 2) - 1), -1, 1)

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
    
# DO NOT MODIFY: Register start and update and begin execution
if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
