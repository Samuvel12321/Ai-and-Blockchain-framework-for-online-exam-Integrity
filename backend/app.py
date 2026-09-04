from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2

from camera_service import camera_service
from ai_engine import AIEngine
from violation_logger import violation_logger
from proctoring_manager import proctoring_manager
from exam_session import exam_session
from session_manager import session_manager


app = Flask(__name__)
CORS(app)


# ============================================================
# AI ENGINE
# ============================================================

print("[AI] Initializing AI Engine...")

ai_engine = AIEngine()

print("[AI] AI Engine ready")


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "status": "success",
        "message": "EduView Backend is running",
        "camera": camera_service.is_running(),
        "ai": True
    })


# ============================================================
# CAMERA START
# ============================================================

@app.route("/api/camera/start", methods=["POST"])
def start_camera():

    success = camera_service.start()

    if success:

        return jsonify({
            "status": "success",
            "message": "Camera started"
        })

    return jsonify({
        "status": "error",
        "message": "Failed to open camera"
    }), 500


# ============================================================
# CAMERA STOP
# ============================================================

@app.route("/api/camera/stop", methods=["POST"])
def stop_camera():

    camera_service.stop()

    return jsonify({
        "status": "success",
        "message": "Camera stopped"
    })


# ============================================================
# CAMERA STATUS
# ============================================================

@app.route("/api/camera/status")
def camera_status():

    return jsonify({
        "running": camera_service.is_running()
    })


# ============================================================
# AI STATUS
# ============================================================

@app.route("/api/ai/status")
def ai_status():

    return jsonify(
        ai_engine.get_detection_data()
    )


# ============================================================
# LIVE VIDEO STREAM
# ============================================================

@app.route("/api/proctoring/status")
def proctoring_status():

    return jsonify(
        ai_engine.get_proctoring_status()
    )

#proctoring status

@app.route("/api/violations")
def get_violations():

    return jsonify({
        "count": violation_logger.get_event_count(),
        "events": violation_logger.get_events()
    })
#violations

@app.route("/api/violations/count")
def get_violation_count():

    return jsonify({
        "count": violation_logger.get_event_count()
    })

#Violations count

@app.route("/api/proctoring/events")
def proctoring_events():

    return jsonify(
        proctoring_manager.get_status()
    )
#Proctoring event

@app.route("/api/proctoring/reset", methods=["POST"])
def reset_proctoring():

    proctoring_manager.reset()

    return jsonify({
        "status": "success",
        "message": "Proctoring session reset"
    })

#Proctoring_Manager

#Exam session management

@app.route("/api/exam/start", methods=["POST"])
def start_exam():

    result = exam_session.start(
        student_id="STUDENT001",
        exam_id="EXAM001"
    )

    if result["status"] == "error":
        return jsonify(result), 400

    return jsonify(result)

#start Exam

@app.route("/api/exam/stop", methods=["POST"])
def stop_exam():

    result = exam_session.stop()

    if result["status"] == "error":
        return jsonify(result), 400

    return jsonify(result)

#Stop Exam

@app.route("/api/exam/status")
def exam_status():

    return jsonify(
        exam_session.get_status()
    )

#Exam Status

@app.route("/api/session/start", methods=["POST"])
def start_session():

    result = session_manager.start_session()

    if result["status"] == "success":

        return jsonify(result)

    return jsonify(result), 400

#SESSION START

@app.route("/api/session/end", methods=["POST"])
def end_session():

    result = session_manager.end_session()

    if result["status"] == "success":

        return jsonify(result)

    return jsonify(result), 400

#SESSION END

@app.route("/api/session/status")
def session_status():

    session = session_manager.get_active_session()

    if session is None:

        return jsonify({
            "active": False,
            "session": None
        })


    return jsonify({
        "active": True,
        "session": session
    })

#SESSION STATUS

@app.route("/api/session/history")
def session_history():

    return jsonify({
        "count": len(
            session_manager.get_session_history()
        ),
        "sessions": session_manager.get_session_history()
    })

#SESSION HISTORY

# ============================================================
# BLOCKCHAIN EXAM HISTORY
# ============================================================

@app.route("/api/blockchain/history")
def blockchain_history():

    sessions = session_manager.get_session_history()

    verified_sessions = []

    for session in sessions:

        session_data = session.copy()

        session_id = session.get("session_id")

        try:

            verification = (
                session_manager.verify_session_integrity(
                    session_id
                )
            )

            if verification.get("success"):

                session_data["integrity"] = (
                    verification.get("status")
                )

            else:

                session_data["integrity"] = "NOT_VERIFIED"

        except Exception as e:

            print(
                "[Blockchain] Verification error:",
                str(e)
            )

            session_data["integrity"] = "ERROR"

        verified_sessions.append(
            session_data
        )

    return jsonify({

        "count": len(verified_sessions),

        "sessions": verified_sessions

    })

# ============================================================
# BLOCKCHAIN SESSION VERIFICATION
# ============================================================

@app.route(
    "/api/blockchain/verify/<session_id>",
    methods=["GET"]
)
def verify_blockchain_session(session_id):

    result = (
        session_manager.verify_session_integrity(
            session_id
        )
    )

    if not result.get("success"):

        return jsonify(result), 404

    return jsonify(result)


# PROCTORING STATUS
def generate_frames():

    while camera_service.is_running():

        frame = camera_service.get_frame()

        if frame is None:
            continue

        # ----------------------------------------------------
        # AI PROCESSING
        # ----------------------------------------------------

        processed_frame = ai_engine.process_frame(frame)

        # ----------------------------------------------------
        # ENCODE FRAME
        # ----------------------------------------------------

        success, buffer = cv2.imencode(
            ".jpg",
            processed_frame
        )

        if not success:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


# ============================================================
# VIDEO FEED
# ============================================================

@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("EduView Custom Backend")
    print("=" * 60)

    print("Server: http://localhost:5000")
    print("Camera API: http://localhost:5000/api/camera/start")
    print("Camera Status: http://localhost:5000/api/camera/status")
    print("AI Status: http://localhost:5000/api/ai/status")
    print("Video: http://localhost:5000/video_feed")
    print("Proctoring status: http://localhost:5000/api/proctoring/status")
    print("Violations: http://localhost:5000/api/violations")
    print("Violations count: http://localhost:5000/api/violations/count")
    print("Proctoring_Manager: http//localhost:5000/api/proctoring/events")
    print("Exam Status: http://localhost:5000/api/exam/status")
    
    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        threaded=True
    )