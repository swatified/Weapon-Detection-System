from flask import Flask, render_template, Response, jsonify
from camera import VideoCamera
import cv2
import time

# Initialize Flask app
app = Flask(__name__)

def gen(camera):
    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            time.sleep(0.01)  # Small delay to prevent overwhelming the browser
    except Exception as e:
        print(f"Error in video feed: {str(e)}")
        yield b''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    try:
        return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Video feed error: {str(e)}")
        return str(e), 500

@app.route('/check_camera')
def check_camera():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({'status': 'error', 'message': 'Could not open camera'})
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return jsonify({'status': 'error', 'message': 'Could not read from camera'})
        return jsonify({'status': 'success', 'message': 'Camera is working'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/check_camera_permissions')
def check_camera_permissions():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({
                'status': 'error',
                'message': 'Could not access camera. Please check permissions.'
            })
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return jsonify({
                'status': 'error',
                'message': 'Could not read from camera. Please check permissions.'
            })
            
        return jsonify({
            'status': 'success',
            'message': 'Camera access granted'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)