# clientTWO.py
import asyncio
import websockets
import cv2
import base64
import time
import json
from camera import get_frame  # <- Use shared camera

async def send_frames():
    uri = "ws://172.20.10.2:8765"
    async with websockets.connect(uri,
                                  ping_interval=None,
                                  ping_timeout=None
                                  ) as websocket:
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

if __name__ == "__main__":
    asyncio.run(send_frames())

