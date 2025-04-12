import cv2 as cv
import numpy as np

def is_obstacle_ahead(frame, min_area=2000):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv.threshold(blurred, 60, 255, cv.THRESH_BINARY_INV)

    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > min_area:
            return True
    return False

# 🧪 Test loop goes here
if __name__ == "__main__":
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera error.")
            break

        if is_obstacle_ahead(frame):
            print("Obstacle ahead!")
        else:
            print("Path is clear.")

        cv.imshow("Obstacle Detection", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
