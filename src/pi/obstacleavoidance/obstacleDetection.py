import cv2 as cv
import numpy as np
import time
from pi.motors.motor import move, stop, cleanup

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

if __name__ == "__main__":
    cap = cv.VideoCapture(0)

    try:
        print("[🟢] Smooth obstacle avoidance loop (press 'q' to quit).")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Camera error.")
                break

            direction = get_obstacle_direction(frame)

            if direction == "left":
                print("[⬅️] Obstacle on left – veering right.")
                move(70, 50)  # turn right slightly
            elif direction == "right":
                print("[➡️] Obstacle on right – veering left.")
                move(50, 70)  # turn left slightly
            elif direction == "center":
                print("[🚧] Obstacle dead ahead – braking and veering.")
                move(-30, 30)  # spin or hard turn
                time.sleep(0.3)
                stop()
            else:
                print("[✅] Path clear – moving forward.")
                move(60, 60)

            cv.imshow("Obstacle Avoidance", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv.destroyAllWindows()
        stop()
        cleanup()
