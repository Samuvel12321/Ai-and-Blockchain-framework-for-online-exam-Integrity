import cv2
import time
from ultralytics import YOLO

MODEL_PATH = "object_cheating/models/modelv11.pt"

print("=" * 50)
print("EduView Standalone Camera + YOLO Test")
print("=" * 50)

print("\n[1] Loading YOLO model...")
model = YOLO(MODEL_PATH)
print("    YOLO loaded successfully!")
print("    Classes:", model.names)

print("\n[2] Opening camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()

print("    Camera opened successfully!")

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("\n[3] Starting real-time detection...")
print("    Press Q to quit.")
print("-" * 50)

frame_count = 0
start_time = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read frame.")
        break

    frame_count += 1

    # YOLO detection
    results = model(
        frame,
        conf=0.5,
        iou=0.5,
        verbose=False
    )

    # Draw detections
    annotated_frame = results[0].plot()

    # FPS calculation
    elapsed = time.time() - start_time

    if elapsed > 0:
        fps = frame_count / elapsed
    else:
        fps = 0

    # Display FPS
    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Display
    cv2.imshow(
        "EduView - AI Proctoring Test",
        annotated_frame
    )

    # Quit
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("\n" + "=" * 50)
print("Test finished.")
print("Frames processed:", frame_count)
print("Average FPS:", round(fps, 2))
print("=" * 50)