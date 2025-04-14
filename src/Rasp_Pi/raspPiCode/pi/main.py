# main.py
import asyncio
import time
import cv2
import base64
import json
import websockets

from camera import get_frame
from markerDetectionPiCam import detect_marker
from motors import init, move, stop, cleanup

# PID Controller
class PIDController:
    def __init__(self, kp=0.1, ki=0.0, kd=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0

    def calculate(self, error):
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

pid = PIDController(kp=0.1, ki=0.0, kd=0.02)

# Tuning thresholds
CENTER_TOLERANCE = 60
SIZE_THRESHOLD = 300

# 🧠 Motion control loop
async def control_loop():
    try:
        print("[🧠] Starting motion tracking loop.")
        init()
    
        last_decision_time = time.time()

        while True:
            frame = get_frame()
            marker = detect_marker(frame)

            current_time = time.time()

            if current_time - last_decision_time >= 1:
                last_decision_time = current_time

                if marker is None:
                    print("[🔍] No marker detected — idling.")
                    stop()
                else:
                    x, y, size = marker
                    print(f"[🎯] Marker at ({x}, {y}), size={size}")

                    center_x = frame.shape[1] // 2
                    error = x - center_x

                    is_centered = abs(error) < CENTER_TOLERANCE
                    is_close = size > SIZE_THRESHOLD

                    if is_centered and is_close:
                        print("[🟡] Marker is close and centered — idling.")
                        stop()
                    else:
                        turn_speed = int(pid.calculate(error) * 1.5)
                        turn_speed = max(min(turn_speed, 50), -50)

                        base_speed = int((SIZE_THRESHOLD - size) * 0.5)
                        base_speed = max(40, min(80, base_speed))

                        def apply_min_duty(speed, min_duty=75):
                            if speed > 0:
                                return max(speed, min_duty)
                            elif speed < 0:
                                return min(speed, -min_duty)
                            else:
                                return 0

                    left_speed = apply_min_duty(base_speed + turn_speed)
                    right_speed = apply_min_duty(base_speed - turn_speed)

                    adjusted_left = (left_speed * 1.125)
                    adjusted_right = (right_speed * 1)

                    print(f"[⚙️] Moving: L={left_speed}, R={right_speed}")
                    move(adjusted_left, adjusted_right)

            await asyncio.sleep(0.01)

    finally:
        print("[⚠️] Cleanup triggered.")
        stop()
        cleanup()

# 📡 Frame streamer (copied from clientTWO.py)
async def send_frames():
    uri = "<IP ADDR of SERVER"
    try:
        async with websockets.connect(uri, ping_interval=None, ping_timeout=None) as websocket:
            print("[📡] WebSocket connected.")
            while True:
                frame = get_frame()
                _, buffer = cv2.imencode('.jpg', frame)
                encoded = base64.b64encode(buffer).decode('utf-8')

                package = {
                    "type": "image",
                    "value": encoded
                }

                json_msg = json.dumps(package)
                await websocket.send(json_msg)
                await asyncio.sleep(0.03)
    except Exception as e:
        print(f"[⚠️] WebSocket streaming error: {e}")

# 🔁 Run both loops together
async def main():
    await asyncio.gather(
        control_loop(),
        send_frames()
    )

if __name__ == "__main__":
    asyncio.run(main())

