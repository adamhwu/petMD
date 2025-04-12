import cv2 as cv
import numpy as np

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

# Initialize camera
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("❌ Failed to open Pi Camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame.")
        break

    result = detect_marker(frame)
    if result:
        x, y, dist = result
        print(f"Marker detected at ({x}, {y}), approx. size: {dist}")

        # Optional: draw marker center
        cv.circle(frame, (x, y), 6, (0, 255, 0), -1)

    # Optional: show window (only works with GUI / monitor)
    cv.imshow("PiCam ArUco", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
