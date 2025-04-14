import cv2 as cv
from computervision.markerDetectionPiCam import detect_marker
from motors.motor import move, stop  # ✅ use real motor control

class PIDController:
    def __init__(self, kp=0.1, ki=0.0, kd=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0

    def reset(self):
        self.integral = 0
        self.prev_error = 0

    def calculate(self, error):
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

def follow_marker():
    cap = cv.VideoCapture(0)
    print("[🟢] Starting marker-following loop (press 'q' to quit).")

    pid = PIDController(kp=0.1, ki=0.0, kd=0.02)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera read failed")
            break

        marker = detect_marker(frame)

        if marker:
            x, y, distance = marker
            print(f"[🎯] Marker detected: x={x}, y={y}, d={distance}")

            center_x = 960
            error = x - center_x
            turn_speed = int(pid.calculate(error))
            base_speed = max(0, min(100, int((distance - 140) * 0.5)))

            left_speed = base_speed - turn_speed
            right_speed = base_speed + turn_speed

            move(left_speed, right_speed)
        else:
            print("[ ] No marker detected.")
            stop()

        cv.imshow("Marker Tracking", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
    stop()

if __name__ == "__main__":
    follow_marker()
