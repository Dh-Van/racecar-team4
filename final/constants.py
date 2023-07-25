REAL = False

SAFE_SPEED = 0.15

"""
Velocity Control Constants
"""
#region
if(REAL):
    LF_IMG_CROP = ((175, 50), (240, 250))
    LF_STRAIGHT_IMG_CROP = ((0, 140), (150, 180))
    LF_SPEED = 0.13
    LF_STRAIGHT_SPEED = 0.16
    LF_kP = 0.15

if(not REAL):
    LF_IMG_CROP = ((300, 0), (480, 640))
    LF_STRAIGHT_IMG_CROP = (((480 // 2), (640 // 2) - 50), ((480 // 2) + 100, (640 // 2) + 50))
    LF_SPEED = 0.5
    LF_STRAIGHT_SPEED = 0.5
    LF_kP = 4.5
#endregion

"""
Camera Constants
"""
if(REAL):
    WIDTH = 320
if(not REAL):
    WIDTH = 640

"""
HSV Constants
"""
# region
if(REAL):
    RED_CONE = ((175, 100, 100), (19, 255, 255))
    BLUE_CONE = ((131, 55, 17), (169, 188, 255))
    BLUE_LINE = ((90,70,70), (110,255,255))
    RED_LINE = ((170,100,100), (10,255,255))
    GREEN_LINE = ((68, 50, 60), (69, 81, 255))
    ORANGE_LINE = ((0,254,254), (1,255,255))
    YELLOW_LINE = ((16, 54, 18), (32, 211, 255))
if(not REAL):
    BLUE_LINE = ((90, 100, 100), (110, 255, 255))
    RED_LINE = ((170, 200, 200), (10, 255, 255))
    GREEN_LINE = ((50, 100, 100), (80, 255, 255))
    ORANGE_LINE = ((0,254,254), (1,255,255))
    YELLOW_LINE = ((16, 54, 18), (32, 211, 255))

# endregion