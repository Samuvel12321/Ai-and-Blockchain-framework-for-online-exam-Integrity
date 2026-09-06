import time
from datetime import datetime

class ProctoringManager:
    def __init__(self):
        self.events = []
        self.risk_score = 0
        self.risk_level = "LOW"

        # Prevent continuous recording of the same frame
        self.last_event_class = None
        self.last_event_time = 0
        self.event_cooldown = 4

        # Unified Risk Points for Model 1, 2, and 3
        self.risk_points = {
            "Normal": 0,
            "normal": 0,
            "center": 0,          # Model 3: Looking at screen
            "Wave": 5,
            "Look Around": 10,
            "left": 10,           # Model 3: Looking left
            "right": 10,          # Model 3: Looking right
            "side": 15,           # Model 3: Looking side for long duration
            "closed": 15,         # Model 3: Eyes closed
            "Bend Over The Desk": 15,
            "Hand Under Table": 20,
            "Stand Up": 25,
            "cheating": 30        # Model 2: Detected cheating object/behavior
        }

    def process_detection(self, detection_data):
        if not detection_data:
            return

        detections = detection_data.get("detections", [])
        if not detections:
            return

        highest_class = detection_data.get("highest_class", "N/A")
        highest_confidence = detection_data.get("highest_confidence", 0)

        if highest_class == "N/A":
            return

        current_time = time.time()

        # Cooldown check
        if (highest_class == self.last_event_class and 
            current_time - self.last_event_time < self.event_cooldown):
            return

        self.last_event_class = highest_class
        self.last_event_time = current_time

        points = self.risk_points.get(highest_class, 0)

        # Ignore completely normal behavior
        if highest_class.lower() in ["normal", "center"]:
            return

        self.risk_score += points
        self.risk_score = min(self.risk_score, 100)

        if points >= 25:
            severity = "CRITICAL"
        elif points >= 15:
            severity = "HIGH"
        elif points >= 10:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        self._update_risk_level()

        event = {
            "id": len(self.events) + 1,
            "event": highest_class,
            "confidence": highest_confidence,
            "severity": severity,
            "risk_points": points,
            "risk_score": self.risk_score,
            "timestamp": datetime.now().isoformat()
        }

        self.events.append(event)
        print(f"[PROCTORING] {highest_class} | Conf: {highest_confidence}% | Risk: {self.risk_score} ({self.risk_level})")

    def _update_risk_level(self):
        if self.risk_score >= 70:
            self.risk_level = "CRITICAL"
        elif self.risk_score >= 45:
            self.risk_level = "HIGH"
        elif self.risk_score >= 20:
            self.risk_level = "MEDIUM"
        else:
            self.risk_level = "LOW"

    def get_status(self):
        return {
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "event_count": len(self.events),
            "events": self.events[-20:]
        }

    def reset(self):
        self.events = []
        self.risk_score = 0
        self.risk_level = "LOW"
        self.last_event_class = None
        self.last_event_time = 0
        print("[PROCTORING] Session reset")

proctoring_manager = ProctoringManager()