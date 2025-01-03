import cv2
import numpy as np
import os
import sys

def load_yolo_model(weights_path, config_path):
    try:
        net = cv2.dnn.readNet(weights_path, config_path)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        return net
    except Exception as e:
        print(f"Error loading YOLO model: {e}")
        sys.exit(1)

def process_frame(img, net, classes):
    try:
        height, width, channels = img.shape
        
        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        outs = net.forward(output_layers)

        # Showing information on the screen
        class_ids = []
        confidences = []
        boxes = []

        # Detecting objects
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

        return boxes, confidences, class_ids, colors
    except Exception as e:
        print(f"Error processing frame: {e}")
        return [], [], [], []

def draw_detections(img, boxes, confidences, class_ids, classes, colors):
    try:
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        if len(indexes) > 0:
            print("Weapon detected in frame")
            
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        
        return img
    except Exception as e:
        print(f"Error drawing detections: {e}")
        return img

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Update paths to be relative
    weights_path = os.path.join(current_dir, "weights", "yolov3_training_2000.weights")
    config_path = os.path.join(current_dir, "weights", "yolov3_testing.cfg")
    
    # Check if model files exist
    if not os.path.exists(weights_path) or not os.path.exists(config_path):
        print(f"Error: YOLO model files not found!")
        print(f"Looking for:")
        print(f"- {weights_path}")
        print(f"- {config_path}")
        sys.exit(1)

    # Initialize model
    net = load_yolo_model(weights_path, config_path)
    classes = ["Weapon"]

    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture device!")
        sys.exit(1)

    try:
        while True:
            ret, img = cap.read()
            if not ret:
                print("Error: Could not read frame!")
                break

            # Process frame
            boxes, confidences, class_ids, colors = process_frame(img, net, classes)
            
            # Draw detections
            img = draw_detections(img, boxes, confidences, class_ids, classes, colors)

            # Display result
            cv2.imshow("Weapon Detection", img)

            # Check for ESC key
            key = cv2.waitKey(1)
            if key == 27:  # ESC key
                break

    except KeyboardInterrupt:
        print("Stopping detection...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()