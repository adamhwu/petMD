import cv2
import numpy as np
from simple_pid import PID
import RPi.GPIO as GPIO
import time

# ========== GPIO SETUP ==========
LEFT_MOTOR_PIN = 6
RIGHT_MOTOR_PIN = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_MOTOR_PIN, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PIN, GPIO.OUT)

left_pwm = GPIO.PWM(LEFT_MOTOR_PIN, 1000)
right_pwm = GPIO.PWM(RIGHT_MOTOR_PIN, 1000)
left_pwm.start(0)
right_pwm.start(0)

# ========== PID SETUP ==========
FOLLOW_DISTANCE = 186
CENTER_X = 960

distance_pid = PID(Kp=1.2, Ki=0, Kd=0, setpoint=FOLLOW_DISTANCE)
distance_pid.output_limits = (0, 100)  # 0–100% duty cycle

yaw_pid = PID(Kp=0.15, Ki=0.1, Kd=0, setpoint=CENTER_X)
yaw_pid.output_limits = (-100, 100)

# ========== CAMERA SETUP ==========
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# ArUco setup
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# ========== CONTROL LOGIC ==========
def move(left_speed, right_speed):
    left_pwm.ChangeDutyCycle(max(0, min(100, left_speed)))
    right_pwm.ChangeDutyCycle(max(0, min(100, right_speed)))

def stop():
    left_pwm.ChangeDutyCycle(0)
    right_pwm.ChangeDutyCycle(0)

last_seen_time = time.time()
DROPOUT_TIMEOUT = 2  # seconds

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera error.")
            stop()
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = detector.detectMarkers(gray)

        if ids is not None:
            last_seen_time = time.time()
            for marker_corners in corners:
                # Calculate center
                x = int((marker_corners[0][0][0] + marker_corners[0][2][0]) / 2)
                y = int((marker_corners[0][0][1] + marker_corners[0][2][1]) / 2)

                # Approximate distance
                size1 = np.linalg.norm(marker_corners[0][0] - marker_corners[0][2])
                size2 = np.linalg.norm(marker_corners[0][1] - marker_corners[0][3])
                distance = (size1 + size2) / 2

                # PID output
                forward_speed = distance_pid(distance)
                yaw_correction = yaw_pid(x)

                left_speed = forward_speed - yaw_correction
                right_speed = forward_speed + yaw_correction

                print(f"[✓] Marker at x={x}, y={y}, distance={int(distance)}")
                print(f"Motor L={int(left_speed)} R={int(right_speed)}")

                move(left_speed, right_speed)
                break  # Only follow first marker

        else:
            if time.time() - last_seen_time > DROPOUT_TIMEOUT:
                print("[!] Marker lost. Stopping.")
                stop()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    stop()
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
