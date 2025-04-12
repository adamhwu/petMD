import cv2 as cv
import time
from computervision.markerDetectionPiCam import get_marker_data
from computervision.obstacleDetection import is_obstacle_ahead

# Stub for checking if GPS fallback is available
def gps_available():
    # Replace with logic to check for GPS data from ESP32
    return False

# Stub for using GPS to move toward pet
def navigate_to_pet_via_gps():
    print("[🔁] Navigating to pet via GPS fallback...")

# Stub for motor control functions
def move_forward():
    print("[🚗] Moving forward")

def turn_left():
    print("[↩️] Turning left to avoid obstacle")

def stop():
    print("[🛑] Stopping rover")

def idle_or_search():
    print("[🔎] Searching for marker...")

# Main loop
def main():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("[❌] Could not open camera.")
        return

    print("[✅] Rover started. Press 'q' to quit.")
    last_seen_time = time.time()
    dropout_timeout = 3  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[❌] Camera read failed.")
            break

        # 1. Check for ArUco marker
        marker_data, _ = get_marker_data(frame)

        if marker_data:
            x, y, distance = marker_data
            print(f"[🎯] Marker detected: x={x}, y={y}, dist={distance}")

            if is_obstacle_ahead(frame):
                print("[🧱] Obstacle ahead detected.")
                turn_left()
            else:
                move_forward()

            last_seen_time = time.time()

        elif gps_available():
            navigate_to_pet_via_gps()

        elif time.time() - last_seen_time > dropout_timeout:
            stop()
            idle_or_search()

        # Display camera feed for debug
        cv.imshow("Rover View", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            print("[👋] Exiting...")
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
