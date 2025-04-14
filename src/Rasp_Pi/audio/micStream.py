import sounddevice as sd
import socketio
import numpy as np

sio = socketio.Client()
sio.connect('http://<PI_IP>:5000')  # Replace with actual Pi IP or hostname

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    sio.emit('mic_audio', indata.tobytes())

with sd.InputStream(samplerate=16000, channels=1, dtype='int16', callback=audio_callback):
    print("🎙️ Mic stream active — press Ctrl+C to stop.")
    while True:
        pass
