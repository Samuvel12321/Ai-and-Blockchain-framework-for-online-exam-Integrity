import cv2
import threading
import time


class CameraService:
    def __init__(self):
        self.camera = None
        self.running = False
        self.lock = threading.Lock()
        self.latest_frame = None

    def start(self):
        if self.running:
            return True

        print("[Camera] Opening camera...")

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            print("[Camera] Failed to open camera")
            self.camera = None
            return False

        # Set resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.running = True

        self.thread = threading.Thread(
            target=self._capture_loop,
            daemon=True
        )

        self.thread.start()

        print("[Camera] Camera started successfully")

        return True

    def _capture_loop(self):
        while self.running:

            if self.camera is None:
                break

            ret, frame = self.camera.read()

            if not ret:
                print("[Camera] Failed to read frame")
                time.sleep(0.05)
                continue

            with self.lock:
                self.latest_frame = frame

        print("[Camera] Capture loop stopped")

    def get_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None

            return self.latest_frame.copy()

    def stop(self):
        print("[Camera] Stopping camera...")

        self.running = False

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        with self.lock:
            self.latest_frame = None

        print("[Camera] Camera stopped")

    def is_running(self):
        return self.running


camera_service = CameraService()