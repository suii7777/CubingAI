from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
import cv2
import numpy as np
from scramble_generator import ScrambleGenerator
import base64
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Global variables
camera = None
is_recording = False
recorded_frames = []
recording_start_time = None

def generate_frames():
    global camera, is_recording, recorded_frames
    while True:
        if camera is None or not camera.isOpened():
            break
            
        success, frame = camera.read()
        if not success:
            break
        else:
            if is_recording:
                recorded_frames.append(frame.copy())
            
            # Convert frame to jpg
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Yield the frame in bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('start_camera')
def start_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            socketio.emit('camera_status', {'status': 'started'})
        else:
            socketio.emit('camera_status', {'status': 'error'})

@socketio.on('stop_camera')
def stop_camera():
    global camera, is_recording
    if is_recording:
        stop_recording()
    if camera is not None:
        camera.release()
        camera = None
    socketio.emit('camera_status', {'status': 'stopped'})

@socketio.on('start_recording')
def start_recording():
    global is_recording, recorded_frames, recording_start_time
    if not is_recording:
        recorded_frames = []
        recording_start_time = time.time()
        is_recording = True
        socketio.emit('recording_status', {'status': 'started'})

@socketio.on('stop_recording')
def stop_recording():
    global is_recording, recorded_frames, recording_start_time
    if is_recording:
        is_recording = False
        if recording_start_time is not None:
            solve_time = time.time() - recording_start_time
            analysis = analyze_solve(solve_time)
            socketio.emit('solve_analysis', analysis)
        socketio.emit('recording_status', {'status': 'stopped'})

@socketio.on('get_scramble')
def get_scramble():
    scramble_gen = ScrambleGenerator()
    scramble, explanations = scramble_gen.get_scramble_with_explanation()
    socketio.emit('scramble', {
        'scramble': scramble,
        'explanations': explanations
    })

def analyze_solve(solve_time):
    return {
        'solve_time': f"{solve_time:.2f}",
        'suggestions': [
            "Practice F2L lookahead to reduce pauses",
            "Consider learning advanced PLL algorithms",
            "Work on finger tricks for faster execution"
        ]
    }

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
