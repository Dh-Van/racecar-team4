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
    SAFE_SPEED = 0.15

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
    LF_IMG_CROP = ((175, 50), (240, 250))
    """
    The image crop for looking ahead of the racecar. This allows us to speed up and slow down
    based on if the current color is seen
    """
    LF_STRAIGHT_IMG_CROP = ((0, 140), (150, 180))
    """
    The default line following speed
    """
    LF_SPEED = 0.13
    """
    Line following speed used when a long straight has been seen
    """
    LF_STRAIGHT_SPEED = 0.16
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
    LF_kP = 0.15

if(not REAL):
    """
    The default image crop for the line following algorithim
    """
    LF_IMG_CROP = ((300, 0), (480, 640))
    """
    The image crop for looking ahead of the racecar. This allows us to speed up and slow down
    based on if the current color is seen
    """
    LF_STRAIGHT_IMG_CROP = (((480 // 2), (640 // 2) - 50), ((480 // 2) + 100, (640 // 2) + 50))
    """
    The default line following speed
    """
    LF_SPEED = 0.5
    """
    Line following speed used when a long straight has been seen
    """
    LF_STRAIGHT_SPEED = 0.5
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
Camera Constants
"""
#region
if(REAL):
    """
    Resolution of the camera being used
    """
    WIDTH = 320
    HEIGHT = 240

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
    RED_CONE = ((175, 100, 100), (19, 255, 255))
    BLUE_CONE = ((131, 55, 17), (169, 188, 255))
    # Lines
    BLUE_LINE = ((90,70,70), (110,255,255))
    RED_LINE = ((170,100,100), (10,255,255))
    GREEN_LINE = ((68, 50, 60), (69, 81, 255))
    ORANGE_LINE = ((0,254,254), (1,255,255))
    YELLOW_LINE = ((16, 54, 18), (32, 211, 255))

if(not REAL):
    # Cones
    # Lines
    BLUE_LINE = ((90, 100, 100), (110, 255, 255))
    RED_LINE = ((170, 200, 200), (10, 255, 255))
    GREEN_LINE = ((50, 100, 100), (80, 255, 255))
    ORANGE_LINE = ((0,254,254), (1,255,255))
    YELLOW_LINE = ((16, 54, 18), (32, 211, 255))

HSV_NOTHING = ((0,0,0), (0,0,0))
HSV_EVERYTHING = ((0, 0, 0), (179, 255, 255))
# endregion