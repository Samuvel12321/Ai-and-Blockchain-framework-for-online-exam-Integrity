import os
import sys
import time
import cv2
import numpy as np
from ultralytics import YOLO

# Add project root to sys.path so we can import the original eye_tracker
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from object_cheating.utils.eye_tracker import EyeTracker

class AIEngine:
    def __init__(self, model1_path="object_cheating/models/modelv11.pt", model2_path="object_cheating/models/modelv8-2.pt"):
        print("=" * 60)
        print("Loading EduView AI Models (Models 1, 2, and 3)")
        print("=" * 60)

        # Resolve paths
        self.m1_path = os.path.join(PROJECT_ROOT, model1_path) if not os.path.isabs(model1_path) else model1_path
        self.m2_path = os.path.join(PROJECT_ROOT, model2_path) if not os.path.isabs(model2_path) else model2_path

        # Load Model 1 (Behavior)
        self.model1 = YOLO(self.m1_path)
        print("YOLO Model 1 loaded successfully!")

        # Load Model 2 (Cheating / Objects)
        self.model2 = YOLO(self.m2_path)
        print("YOLO Model 2 loaded successfully!")

        # Load Model 3 (Eye Tracking & Gaze)
        self.eye_tracker = EyeTracker()
        print("MediaPipe + Keras Model 3 loaded successfully!")
        
        self.conf_threshold = 0.50
        self.alert_counter = 0
        self.frame_counter = 0

        self.last_detection = {
            "count": 0,
            "highest_class": "N/A",
            "highest_confidence": 0.0,
            "processing_time": 0.0,
            "detections": []
        }

    def process_frame(self, frame):
        if frame is None:
            return frame, self.last_detection

        start_time = time.time()
        self.frame_counter += 1

        # ----------------------------------------------------
        # 1. Inference - Model 3 (Eye Tracking)
        # We run this first because it returns an already-drawn frame
        # ----------------------------------------------------
        (
            processed_frame, alerts, total_eye_det, proc_time_eye, 
            eye_class, eye_conf, eye_coords
        ) = self.eye_tracker.process_eye_detections(
            frame, self.alert_counter, self.frame_counter, 
            cnn_threshold=0.6, duration_threshold=3.0, is_video=True, selected_target="All"
        )

        combined_detections = []
        highest_conf = 0.0
        top_class = "N/A"

        # Helper function to override priority
        def update_highest_priority(new_class, new_conf):
            nonlocal highest_conf, top_class
            is_current_normal = top_class.lower() in ["normal", "center", "n/a"]
            is_new_suspicious = new_class.lower() not in ["normal", "center"]

            if is_new_suspicious and (is_current_normal or new_conf > highest_conf):
                highest_conf = new_conf
                top_class = new_class
            elif is_current_normal and not is_new_suspicious and new_conf > highest_conf:
                highest_conf = new_conf
                top_class = new_class

        # Register Eye Tracking Results
        if eye_class != "N/A":
            normalized_eye_conf = eye_conf / 100.0 # Normalize to 0-1 scale to match YOLO
            combined_detections.append({
                "model": "model_3",
                "class": eye_class,
                "confidence": round(eye_conf, 2),
                "box": [eye_coords["xmin"], eye_coords["ymin"], eye_coords["xmax"], eye_coords["ymax"]]
            })
            update_highest_priority(eye_class, normalized_eye_conf)

        # ----------------------------------------------------
        # 2. Inference - Model 1 (Classroom Behavior)
        # ----------------------------------------------------
        results1 = self.model1(frame, conf=self.conf_threshold, verbose=False)[0]
        for box in results1.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = self.model1.names[cls_id]
            conf = float(box.conf[0].item())
            coords = [int(v) for v in box.xyxy[0].tolist()]

            combined_detections.append({
                "model": "model_1",
                "class": cls_name,
                "confidence": round(conf * 100, 2),
                "box": coords
            })
            update_highest_priority(cls_name, conf)

            # Draw green box
            cv2.rectangle(processed_frame, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 0), 2)
            cv2.putText(processed_frame, f"{cls_name} {conf*100:.1f}%", (coords[0], max(20, coords[1] - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # ----------------------------------------------------
        # 3. Inference - Model 2 (Cheating / Object Detection)
        # ----------------------------------------------------
        results2 = self.model2(frame, conf=self.conf_threshold, verbose=False)[0]
        for box in results2.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = self.model2.names[cls_id]
            conf = float(box.conf[0].item())
            coords = [int(v) for v in box.xyxy[0].tolist()]

            combined_detections.append({
                "model": "model_2",
                "class": cls_name,
                "confidence": round(conf * 100, 2),
                "box": coords
            })
            update_highest_priority(cls_name, conf)

            # Draw orange box
            cv2.rectangle(processed_frame, (coords[0], coords[1]), (coords[2], coords[3]), (0, 140, 255), 2)
            cv2.putText(processed_frame, f"[M2] {cls_name} {conf*100:.1f}%", (coords[0], coords[3] + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 140, 255), 2)

        proc_time = round(time.time() - start_time, 3)

        self.last_detection = {
            "count": len(combined_detections),
            "detections": combined_detections,
            "highest_class": top_class,
            "highest_confidence": round(highest_conf * 100, 1),
            "processing_time": proc_time
        }

        return processed_frame

    def get_proctoring_status(self):
        detection_data = self.last_detection
        highest_class = detection_data["highest_class"]
        confidence = detection_data["highest_confidence"]

        if highest_class in ["N/A", "Normal", "normal", "center"]:
            status = "NORMAL"
            severity = 0
        elif highest_class in ["Look Around", "Wave", "left", "right"]:
            status = "WARNING"
            severity = 1
        elif highest_class in ["Bend Over The Desk", "Hand Under Table", "Stand Up", "cheating", "closed", "side"]:
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