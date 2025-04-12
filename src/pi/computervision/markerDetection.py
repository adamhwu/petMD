import cv2 as cv

# --- ArUco setup ---
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(dictionary, parameters)

def clean_data_string(data):
    """
    Cleans and validates an input string like '123,200,42'
    Returns (x, y, distance) if valid, else None
    """
    cleanout = ''.join(c for c in data if c.isdigit() or c == ',')
    if cleanout.count(',') != 2:
        return None
    try:
        x, y, dist = map(int, cleanout.split(','))
        return x, y, dist
    except:
        return None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    markerCorners, markerIds, _ = detector.detectMarkers(gray)

    if markerIds is not None:
        cv.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

        for corners, markerId in zip(markerCorners, markerIds):
            x_center = int((corners[0][0][0] + corners[0][2][0]) / 2)
            y_center = int((corners[0][0][1] + corners[0][2][1]) / 2)

            size1 = cv.norm(corners[0][0] - corners[0][2])
            size2 = cv.norm(corners[0][1] - corners[0][3])
            marker_distance = int((size1 + size2) / 2)

            # Emulate Arduino's serial output
            raw_data = f"{x_center},{y_center},{marker_distance}"
            print(f"[Raw] {raw_data}")

            # Clean and parse like getSerialCoords.ino
            result = clean_data_string(raw_data)
            if result:
                x, y, dist = result
                print(f"[✓] Success: x={x}, y={y}, distance={dist}")
            else:
                print("[!] Failure - invalid format")

            # Draw center marker
            cv.circle(frame, (x_center, y_center), 5, (0, 255, 0), -1)
    else:
        print("[!] No marker detected")

    # Show output
    cv.imshow("ArUco Tracker", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
