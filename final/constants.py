"""
Sets the module wide simulation constant. This is so that we can easily move
between the sim and real life with just changing 1 value. Ensure that this is 
set to the right value before testing, and also ensure that every simulation
value has a real value, and every real value has a simulation value
"""
REAL = False

"""
Generic System Constants
"""
#region
if(REAL):
    SAFE_SPEED = 0.1

if(not REAL):
    SAFE_SPEED = 0.25
#endregion


"""
Line Following Constants
"""
#region
if(REAL):
    """
    The default image crop for the line following algorithim
    """
    LF_IMG_CROP = ((150, 0), (240, 320))
    """
    The image crop for looking ahead of the racecar. This allows us to speed up and slow down
    based on if the current color is seen
    """
    LF_TURN_SPEED = 0.1095
    """
    The default line following speed
    """
    LF_SPEED = 0.13
    """
    The minimum area for a line to be recognized
    """
    LF_MIN_CONTOUR_AREA = 250
    """
    Proportional gain for the P controller for use with line following
    """
    LF_kP = 0.2

if(not REAL):
    """
    The default image crop for the line following algorithim
    """
    LF_IMG_CROP = ((300, 0), (480, 640))
    """
    The default line following speed
    """
    LF_SPEED = 0.5
    """
    Line following speed used when a long straight has been seen
    """
    LF_TURN_SPEED = 0.11
    """
    The minimum area for a straight to be recognized should be bigger than the minimum
    area for a normal line to be recognized
    """
    LF_MIN_FAST_AREA = 3500
    """
    The minimum area for a line to be recognized
    """
    LF_MIN_CONTOUR_AREA = 500
    """
    Proportional gain for the P controller for use with line following
    """
    LF_kP = 4.5
#endregion

"""
Cone Slaloming Constants
"""

CS_APPROACH_CROP = ((80, 0),(240, 320))
CS_SEARCH_CROP = ((80, 0), (240, 320))
CS_FAST_SPEED = 0.16
CS_SLOW_SPEED = 0.13
CS_AVOID_ANGLE = 1
CS_TURNBACK_ANGLE = -1
CS_FORWARD_WINDOW = (700,20)
CS_LEFT_WINDOW = (520,560)
CS_RIGHT_WINDOW = (160, 200)

"""
Wall Following Constants
"""
#region
if(REAL):
    WF_SPEED_SLOW = 0.15
    WF_SPEED_FAST = 0.175
    WF_SIDE_THRESHOLD = 250
    WF_FRONT_THRESHOLD = 70

    """
    Front Distance, Right Distance, Right Forward Distance, Left Distance, Left Forward Distaance
    """
    WF_WINDOWS = [
        (-20, 20),
        (85, 95),
        (30, 40),
        (265, 275),
        (-40, -30)
    ]

    WF_kP = 0.5
#endregion

"""
Camera Constants
"""
#region
if(REAL):
    """
    Resolution of the camera being used
    """
    WIDTH = 320
    HEIGHT = 240
    MIN_CONE_AREA = 30

if(not REAL):
    """
    Resolution of the camera being used
    """
    WIDTH = 640
    HEIGHT = 480
#endregion

"""
HSV Constants
"""
# region
if(REAL):
    # Cones
    PURPLE_CONE = ((85, 100, 17), (115, 188, 255))
    ORANGE_CONE = ((165, 100, 100), (19, 255, 255))
    # Lines
    BLUE_LINE = ((90,70,70), (110,255,255))
    RED_LINE = ((170,100,100), (10,255,255))
    GREEN_LINE = [(40, 50, 150), (80, 255, 255)]
    ORANGE_LINE = ((0,254,254), (1,255,255))
    YELLOW_LINE = ((16, 54, 18), (32, 211, 255))

if(not REAL):
    # Cones
    RED_CONE = ((170, 50, 50), (10, 255, 255))
    BLUE_CONE = ((80, 100, 100), (130, 255, 255))
    # Lines
    BLUE_LINE = ((90, 100, 100), (110, 255, 255))
    RED_LINE = ((170, 200, 200), (10, 255, 255))
    GREEN_LINE = ((50, 100, 100), (80, 255, 255))
    ORANGE_LINE = ((0,254,254), (1,255,255))
    YELLOW_LINE = ((16, 54, 18), (32, 211, 255))
    PURPLE_LINE = ((110, 17, 128), (140, 255, 255))

    # Borders
    RED_BORDER = ((170, 50, 50), (10, 255, 255))

HSV_NOTHING = ((0,0,0), (0,0,0))
HSV_EVERYTHING = ((0, 0, 0), (179, 255, 255))
# endregion