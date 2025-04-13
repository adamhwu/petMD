# camera.py
from picamera2 import Picamera2
import time

# Initialize and configure Pi Camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
))
picam2.start()
time.sleep(1)

# Public function to get the latest frame
def get_frame():
    return picam2.capture_array()

