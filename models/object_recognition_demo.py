import cv2
import torch
import numpy as np

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/yolov5s.pt')

# Set up video capture
cap = cv2.VideoCapture(0)

# Colors for each class
np.random.seed(543210)
colors = np.random.uniform(0, 255, size=(80, 3))

# Set of seen objects
seen_objects = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)

    detections = []
    for det in results.xyxy[0]:  # xyxy format: [xmin, ymin, xmax, ymax, confidence, class]
        xmin, ymin, xmax, ymax, confidence, class_id = det
        if confidence > 0.2:  # Set confidence threshold
            class_name = model.names[int(class_id)]
            if class_name not in seen_objects:
                detections.append(f"{class_name} ({confidence:.2f})")
                seen_objects.add(class_name)
                
            # Draw bounding box and label
            color = colors[int(class_id)]
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
            label = f"{class_name}: {confidence:.2f}%"
            cv2.putText(frame, label, (int(xmin), int(ymin) - 10 if int(ymin) > 20 else int(ymin) + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    if detections:
        print("I see:", ', '.join(detections))

    # Display the frame
    cv2.imshow('Detected Objects', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):  # Press 'q' to break the loop
        break

cap.release()
cv2.destroyAllWindows()
