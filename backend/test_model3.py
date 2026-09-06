import os
import sys
import time
import cv2

# Set working directory to project root so relative model paths inside EyeTracker work
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)

from object_cheating.utils.eye_tracker import EyeTracker


def test_model3():
    print("=" * 60)
    print("Initializing Model 3: MediaPipe Landmarker + Gaze CNN")
    print("=" * 60)

    try:
        tracker = EyeTracker()
        print("Model 3 loaded successfully!\n")
    except Exception as e:
        print(f"Failed to initialize EyeTracker: {e}")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Unable to open webcam.")
        return

    # Set camera resolution matching the project standard
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    alert_counter = 0
    frame_counter = 0

    print("Camera running. Test gaze: look center, look left, look right, or close eyes.")
    print("Press 'q' in the display window to exit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        frame_counter += 1

        # Process frame through Model 3
        (
            processed_frame,
            alerts,
            total_detections,
            proc_time,
            highest_class,
            highest_conf,
            coords,
        ) = tracker.process_eye_detections(
            frame=frame,
            alert_counter=alert_counter,
            frame_counter=frame_counter,
            cnn_threshold=0.6,
            duration_threshold=3.0,
            is_video=True,
            selected_target="All",
        )

        # Overlay real-time diagnostics on screen
        overlay_text = f"Gaze: {highest_class} ({highest_conf}%) | Alerts: {len(alerts)}"
        cv2.putText(
            processed_frame,
            overlay_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        if alerts:
            for idx, alert in enumerate(alerts):
                cv2.putText(
                    processed_frame,
                    alert,
                    (20, 80 + (idx * 28)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 0, 255),
                    2,
                )

        cv2.imshow("Model 3 - Eye & Gaze Tracker Standalone Test", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[Test Complete] Webcam released.")


if __name__ == "__main__":
    test_model3()