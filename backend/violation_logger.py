import time
from datetime import datetime


class ViolationLogger:

    def __init__(self):
        self.events = []

    def log_event(
        self,
        behaviour,
        severity,
        confidence
    ):

        event = {
            "event_id": len(self.events) + 1,
            "event_type": "PROCTORING_VIOLATION",
            "behaviour": behaviour,
            "severity": severity,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "unix_timestamp": time.time()
        }

        self.events.append(event)

        print("=" * 60)
        print("PROCTORING EVENT")
        print("=" * 60)
        print(f"Event ID    : {event['event_id']}")
        print(f"Behaviour   : {behaviour}")
        print(f"Severity    : {severity}")
        print(f"Confidence  : {confidence}%")
        print(f"Timestamp   : {event['timestamp']}")
        print("=" * 60)

        return event

    def get_events(self):

        return self.events

    def get_event_count(self):

        return len(self.events)


violation_logger = ViolationLogger()