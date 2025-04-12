import cv2 as cv
import time

def main():
    # Open the Pi camera (should be index 0)
    cap = cv.VideoCapture(0)

    # Set resolution if needed (adjust depending on your Pi camera config)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    # Initialize the ArUco detector
    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
    parameters = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(dictionary, parameters)

    print("[INFO] ArUco detection initialized.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture frame")
            break

        # Convert to grayscale for detection
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detect ArUco markers
        markerCorners, markerIds, _ = detector.detectMarkers(gray)

        if markerIds is not None:
            # Draw detected markers
            cv.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

            for corners, markerId in zip(markerCorners, markerIds):
                # Compute marker center
                x_center = int((corners[0][0][0] + corners[0][2][0]) / 2)
                y_center = int((corners[0][0][1] + corners[0][2][1]) / 2)

                # Estimate "distance" based on marker size
                size1 = cv.norm(corners[0][0] - corners[0][2])
                size2 = cv.norm(corners[0][1] - corners[0][3])
                marker_distance = int((size1 + size2) / 2)

                # Output to console
                print(f"[✓] Marker ID: {markerId[0]} | x: {x_center}, y: {y_center}, size: {marker_distance}")

                # Draw center dot
                cv.circle(frame, (x_center, y_center), 5, (0, 255, 0), -1)

        else:
            print("[ ] No marker detected.")

        # Show frame (for debug)
        cv.imshow('Pi ArUco Tracker', frame)

        # Exit if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
