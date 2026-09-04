import cv2
import time
from ultralytics import YOLO


class AIEngine:

    def __init__(self):
        print("=" * 60)
        print("Loading EduView AI Model")
        print("=" * 60)

        self.model = YOLO(
            "object_cheating/models/modelv11.pt"
        )

        print("YOLO Model 1 loaded successfully!")
        print("Classes:")
        print(self.model.names)

        self.last_detection = {
            "count": 0,
            "highest_class": "N/A",
            "highest_confidence": 0.0,
            "processing_time": 0.0,
            "detections": []
        }

    def process_frame(self, frame):

        start_time = time.time()

        results = self.model(
            frame,
            conf=0.40,
            iou=0.45,
            verbose=False
        )

        processed_frame = frame.copy()

        detections = []

        highest_confidence = 0.0
        highest_class = "N/A"

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                confidence = float(box.conf[0])

                class_id = int(box.cls[0])

                class_name = self.model.names[class_id]

                detections.append({
                    "class": class_name,
                    "confidence": round(confidence * 100, 2),
                    "coordinates": {
                        "xmin": int(x1),
                        "ymin": int(y1),
                        "xmax": int(x2),
                        "ymax": int(y2)
                    }
                })

                if confidence > highest_confidence:

                    highest_confidence = confidence

                    highest_class = class_name

                # Draw bounding box

                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)

                cv2.rectangle(
                    processed_frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                label = f"{class_name} {confidence:.2f}"

                cv2.putText(
                    processed_frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        processing_time = time.time() - start_time

        self.last_detection = {
            "count": len(detections),
            "highest_class": highest_class,
            "highest_confidence": round(
                highest_confidence * 100,
                2
            ),
            "processing_time": round(
                processing_time,
                3
            ),
            "detections": detections
        }

        return processed_frame

    def get_proctoring_status(self):

        detection_data = self.last_detection

        highest_class = detection_data["highest_class"]
        confidence = detection_data["highest_confidence"]

        if highest_class == "N/A":
            status = "NORMAL"
            severity = 0

        elif highest_class == "Normal":
            status = "NORMAL"
            severity = 0

        elif highest_class in ["Look Around", "Wave"]:
            status = "WARNING"
            severity = 1

        elif highest_class in [
            "Bend Over The Desk",
            "Hand Under Table",
            "Stand Up"
        ]:
            status = "SUSPICIOUS"
            severity = 2

        else:
            status = "UNKNOWN"
            severity = 0

        return {
            "status": status,
            "severity": severity,
            "behaviour": highest_class,
            "confidence": confidence
        }
    
    def get_detection_data(self):

        return self.last_detection