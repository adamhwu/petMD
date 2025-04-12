import cv2 as cv
from computervision.markerDetectionPiCam import detect_marker

def move(left, right):
    print(f"[MOTORS] Left={left} | Right={right}")

def stop():
    print("[MOTORS] Stopped")

def follow_marker():
    cap = cv.VideoCapture(0)
    print("[🟢] Starting marker-following loop (press 'q' to quit).")

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
            turn_speed = int(error * 0.1)
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
