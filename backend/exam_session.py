import uuid
from datetime import datetime


class ExamSession:

    def __init__(self):

        self.active = False

        self.session_id = None
        self.student_id = None
        self.exam_id = None

        self.start_time = None
        self.end_time = None

    def start(self, student_id="STUDENT001", exam_id="EXAM001"):

        if self.active:
            return {
                "status": "error",
                "message": "An exam session is already active"
            }

        self.session_id = str(uuid.uuid4())

        self.student_id = student_id
        self.exam_id = exam_id

        self.start_time = datetime.now().isoformat()
        self.end_time = None

        self.active = True

        print(
            f"[SESSION] Exam started | "
            f"Session: {self.session_id}"
        )

        return {
            "status": "success",
            "message": "Exam session started",
            "session_id": self.session_id,
            "student_id": self.student_id,
            "exam_id": self.exam_id,
            "start_time": self.start_time
        }

    def stop(self):

        if not self.active:
            return {
                "status": "error",
                "message": "No active exam session"
            }

        self.end_time = datetime.now().isoformat()

        session_data = {
            "status": "success",
            "message": "Exam session ended",
            "session_id": self.session_id,
            "student_id": self.student_id,
            "exam_id": self.exam_id,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

        self.active = False

        print(
            f"[SESSION] Exam ended | "
            f"Session: {self.session_id}"
        )

        return session_data

    def get_status(self):

        return {
            "active": self.active,
            "session_id": self.session_id,
            "student_id": self.student_id,
            "exam_id": self.exam_id,
            "start_time": self.start_time,
            "end_time": self.end_time
        }


exam_session = ExamSession()