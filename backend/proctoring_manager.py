import time
from datetime import datetime


class ProctoringManager:

    def __init__(self):
        self.events = []

        self.risk_score = 0
        self.risk_level = "LOW"

        # Prevent the same detection from being recorded
        # continuously on every AI frame.
        self.last_event_class = None
        self.last_event_time = 0

        # Minimum time between identical events
        self.event_cooldown = 5

        # Risk points for each detected behaviour
        self.risk_points = {
            "Normal": 0,
            "Bend Over The Desk": 15,
            "Hand Under Table": 20,
            "Look Around": 10,
            "Stand Up": 25,
            "Wave": 5
        }

    def process_detection(self, detection_data):

        if not detection_data:
            return

        detections = detection_data.get("detections", [])

        if not detections:
            return

        # Use the highest-confidence detection
        highest_class = detection_data.get(
            "highest_class",
            "N/A"
        )

        highest_confidence = detection_data.get(
            "highest_confidence",
            0
        )

        if highest_class == "N/A":
            return

        current_time = time.time()

        # Avoid recording identical events every frame
        if (
            highest_class == self.last_event_class
            and current_time - self.last_event_time
            < self.event_cooldown
        ):
            return

        self.last_event_class = highest_class
        self.last_event_time = current_time

        # Get risk points
        points = self.risk_points.get(
            highest_class,
            0
        )

        # Normal behaviour should not create an event
        if highest_class == "Normal":
            return

        # Update risk score
        self.risk_score += points

        # Limit score to 100
        self.risk_score = min(
            self.risk_score,
            100
        )

        # Determine severity
        if points >= 25:
            severity = "CRITICAL"
        elif points >= 20:
            severity = "HIGH"
        elif points >= 10:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        # Determine overall risk
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

        print(
            f"[PROCTORING] {highest_class} | "
            f"Confidence: {highest_confidence}% | "
            f"Risk: {self.risk_score} ({self.risk_level})"
        )

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