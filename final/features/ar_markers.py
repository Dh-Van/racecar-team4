import sys, scipy, cv2, numpy as np
sys.path.insert(0, "../../../library")
sys.path.insert(0, "..utils")
from typing import List, Tuple
import constants, math_utils, sensor_utils
from states import States
import racecar_core
import racecar_utils as rc_utils

class ar_scan:

    rc = None
    marker_list = []

    def __init__(self, rc: racecar_core.Racecar) -> None:
        self.rc = rc

    def scan(self):
        image = self.rc.camera.get_color_image()

        aruco_data = cv2.aruco.detectMarkers(
            image,
            cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250),
            parameters=cv2.aruco.DetectorParameters_create()
        )
        
        self.marker_list = self.__get_marker_list(aruco_data)
        
        # rc_utils.draw_ar_markers(image, marker_list)
        # self.rc.display.show_color_image(image)
        
        biggest_marker = self.get_biggest_marker(self.marker_list)
        biggest_marker_id = biggest_marker.get_id() if biggest_marker is not None else 0
        if(biggest_marker_id == 0): print("No marker detected")
        return biggest_marker_id
    
    def get_color(self, marker_list: List[rc_utils.ARMarker], color_range, color_name):
        image = self.rc.camera.get_color_image()
        markers = []
        for m in marker_list:
            color_tuple = [(color_range[0], color_range[1], color_name)]
            m.detect_colors(image, color_tuple)
            if(m.get_color() == color_name): markers.append(m)

        return self.get_biggest_marker(markers)
        

    def get_biggest_marker(self, marker_list):
        biggest = 0, None
        for marker in marker_list:
            size = self.get_size(marker)
            if(size > biggest[0]):
                biggest = size, marker
        return biggest[1]

    def get_size(self, marker: rc_utils.ARMarker):
        corners = marker.get_corners()
        side_len = abs(corners[0][0] - corners[1][0])
        return side_len

    def __get_marker_list(self, aruco_data):
        corners, ids = aruco_data[0], aruco_data[1]
        markers = []    

        for i in range(len(corners)):
            corner = corners[i][0].astype(np.int32)
            for j in range(len(corner)):
                corner[j] = [corner[j][1], corner[j][0]]
            id = ids[i]
            markers.append(rc_utils.ARMarker(id, corner))

        return markers
    
    def get_marker_list(self):
        return self.marker_list