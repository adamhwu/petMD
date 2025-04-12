import sounddevice as sd
import socketio
import numpy as np

sio = socketio.Client()
sio.connect('http://<PI_IP>:5000')

@sio.on('play_audio')
def on_audio(data):
    audio = np.frombuffer(data, dtype='int16')
    sd.play(audio, samplerate=16000)

sio.wait()
