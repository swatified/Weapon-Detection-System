import cv2
import numpy as np
import os
import platform
import time

class VideoCamera:
    def __init__(self):
        try:
            self.video = self.init_camera()
            if not self.video.isOpened():
                raise ValueError("Could not open video device")
            
            # Test first frame
            ret, frame = self.video.read()
            if not ret:
                raise ValueError("Could not read frame from video device")
                
            # Load YOLO
            current_dir = os.path.dirname(os.path.abspath(__file__))
            weights_path = os.path.join(current_dir, "weights", "yolov3_training_2000.weights")
            config_path = os.path.join(current_dir, "weights", "yolov3_testing.cfg")
            
            if not os.path.exists(weights_path) or not os.path.exists(config_path):
                raise FileNotFoundError(f"YOLO model files not found at {weights_path} or {config_path}")
                
            self.net = cv2.dnn.readNet(weights_path, config_path)
            self.classes = ["Weapon"]
            self.layer_names = self.net.getLayerNames()
            self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
            self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
            
            # Set backend and target
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
            print("Camera and YOLO model initialized successfully")
            
        except Exception as e:
            print(f"Error initializing camera: {str(e)}")
            raise

    def init_camera(self):
        """Try different camera indices and settings"""
        indices = [0, 1, 2]  # Common camera indices
        
        for idx in indices:
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                # Set camera properties
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 30)
                
                # Test read
                ret, _ = cap.read()
                if ret:
                    print(f"Successfully opened camera at index {idx}")
                    return cap
                cap.release()
        
        # If no camera works, try platform-specific options
        if platform.system() == 'Windows':
            return cv2.VideoCapture(0, cv2.CAP_DSHOW)
        return cv2.VideoCapture(0)

    def __del__(self):
        if hasattr(self, 'video') and self.video.isOpened():
            self.video.release()
            print("Camera released")

    def get_frame(self):
        """Capture and process a frame from the camera"""
        try:
            success, frame = self.video.read()
            if not success:
                print("Failed to read frame")
                return None
            
            height, width, _ = frame.shape
            
            # Detecting objects
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            # Information to display on screen
            class_ids = []
            confidences = []
            boxes = []

            # Showing information on the screen
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_PLAIN

            # Draw detections on the frame
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    confidence = confidences[i]
                    color = self.colors[class_ids[i]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, f"{label} {confidence:.2f}", (x, y + 30), 
                              font, 2, color, 2)
                    print(f"Detected {label} with confidence {confidence:.2f}")

            # Encode frame to JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                print("Failed to encode frame")
                return None
                
            return jpeg.tobytes()
            
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            return None