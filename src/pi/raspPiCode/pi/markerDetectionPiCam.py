# markerDetectionPiCam.py
import cv2 as cv
import numpy as np
from camera import get_frame  # ✅ Use shared camera access

# Set up the ArUco detector once
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(dictionary, parameters)

def detect_marker(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        for marker in corners:
            x = int((marker[0][0][0] + marker[0][2][0]) / 2)
            y = int((marker[0][0][1] + marker[0][2][1]) / 2)
            size1 = cv.norm(marker[0][0] - marker[0][2])
            size2 = cv.norm(marker[0][1] - marker[0][3])
            distance = int((size1 + size2) / 2)
            return (x, y, distance)
    return None

