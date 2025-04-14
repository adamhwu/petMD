# obstacleDetection.py
import cv2 as cv
import numpy as np
import time
from camera import get_frame  # ✅ Centralized camera access
from motors import move, stop, cleanup

def get_obstacle_direction(frame, min_area=2000):
    """
    Returns: 
    - None if no obstacle
    - "left", "right", or "center" if obstacle detected in that region
    """
    h, w = frame.shape[:2]
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv.threshold(blurred, 60, 255, cv.THRESH_BINARY_INV)

    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > min_area:
            x, y, w_box, h_box = cv.boundingRect(cnt)
            center_x = x + w_box // 2

            if center_x < frame.shape[1] // 3:
                return "left"
            elif center_x > (2 * frame.shape[1]) // 3:
                return "right"
            else:
                return "center"

    return None
