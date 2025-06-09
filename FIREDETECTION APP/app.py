from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import cv2
import base64
import threading
import time
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
detection_active = False
detection_thread = None
camera = None
stats = {
    'total_frames': 0,
    'fire_detected_frames': 0,
    'alerts_sent': 0,
    'last_detection': None
}

def detect_fire(frame):
    """
    Enhanced fire detection using multiple color spaces and contour analysis.
    Returns: (fire_detected: bool, confidence: float)
    """
    try:
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define HSV ranges for fire-like colors
        lower_fire1 = np.array([0, 50, 50])
        upper_fire1 = np.array([30, 255, 255])

        lower_fire2 = np.array([15, 50, 50])
        upper_fire2 = np.array([35, 255, 255])

        # Create masks for fire-like colors
        mask1 = cv2.inRange(hsv, lower_fire1, upper_fire1)
        mask2 = cv2.inRange(hsv, lower_fire2, upper_fire2)
        fire_mask = cv2.bitwise_or(mask1, mask2)

        # Apply morphological operations to reduce noise
        kernel = np.ones((5, 5), np.uint8)
        fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_CLOSE, kernel)
        fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_OPEN, kernel)

        # Find contours for fire regions
        contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return False, 0.0

        # Analyze contours
        total_fire_area = 0
        valid_contours = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Minimum area threshold
                valid_contours += 1
                total_fire_area += area

        if valid_contours == 0:
            return False, 0.0

        # Calculate confidence based on area
        frame_area = frame.shape[0] * frame.shape[1]
        confidence = min((total_fire_area / frame_area) * 100, 100)

        return confidence > 25, confidence
    except Exception as e:
        print(f"Error in fire detection: {e}")
        return False, 0.0

def detection_loop():
    """Main detection loop running in a separate thread."""
    global detection_active, camera, stats

    print("Starting detection loop...")

    # Initialize camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not access camera")
        socketio.emit('detection_error', {'message': 'Could not access camera'})
        return

    while detection_active:
        try:
            ret, frame = camera.read()
            if not ret:
                print("Failed to read frame from camera")
                continue

            stats['total_frames'] += 1
            fire_detected, confidence = detect_fire(frame)

            if fire_detected:
                stats['fire_detected_frames'] += 1
                stats['alerts_sent'] += 1
                stats['last_detection'] = datetime.now().isoformat()
                cv2.putText(frame, f'FIRE DETECTED! Confidence: {confidence:.1f}%',
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.putText(frame, 'No Fire Detected', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('frame_update', {
                'image': frame_base64,
                'fire_detected': fire_detected,
                'confidence': confidence,
                'stats': stats.copy()
            })
            time.sleep(0.1)
        except Exception as e:
            print(f"Error in detection loop: {e}")
            continue

    if camera:
        camera.release()
        camera = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_detection', methods=['POST'])
def start_detection():
    global detection_active, detection_thread
    if detection_active:
        return jsonify({'status': 'error', 'message': 'Detection already active'})
    detection_active = True
    detection_thread = threading.Thread(target=detection_loop, daemon=True)
    detection_thread.start()
    return jsonify({'status': 'success', 'message': 'Detection started'})

@app.route('/api/stop_detection', methods=['POST'])
def stop_detection():
    global detection_active, camera
    detection_active = False
    if camera:
        camera.release()
    return jsonify({'status': 'success', 'message': 'Detection stopped'})

@app.route('/api/upload_and_analyze', methods=['POST'])
def upload_and_analyze():
    if 'files' not in request.files:
        return jsonify({'status': 'error', 'message': 'No files uploaded'})
    files = request.files.getlist('files')
    results = []
    for file in files:
        file_bytes = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if frame is not None:
            fire_detected, confidence = detect_fire(frame)
            results.append({
                'filename': file.filename,
                'fire_detected': fire_detected,
                'confidence': confidence
            })
    return jsonify({'status': 'success', 'results': results})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
