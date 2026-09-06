import cv2
import os
from ultralytics import YOLO

# 1. Define the path to Model 2
# Assuming this script is inside the 'backend' folder and 'object_cheating' is at the same level
MODEL_PATH = "../object_cheating/models/modelv8-2.pt"

def test_model2():
    print(f"Loading Model 2 from: {MODEL_PATH}")
    
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model file not found at {MODEL_PATH}.")
        print("Please check your folder structure.")
        return

    # Load the YOLO model
    model = YOLO(MODEL_PATH)
    print("Model 2 loaded successfully!")
    
    # Print the classes Model 2 was trained to detect
    print("\n--- Model 2 Classes ---")
    print(model.names)
    print("-----------------------\n")

    # 2. Open the Webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        return

    print("Starting webcam stream... Press 'q' in the video window to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # 3. Run Inference with a 50% confidence threshold
        results = model(frame, conf=0.5, verbose=False)[0]

        # 4. Draw the detections on the frame
        for box in results.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = model.names[cls_id]
            conf = float(box.conf[0].item()) * 100
            coords = [int(v) for v in box.xyxy[0].tolist()]

            # Draw an orange bounding box
            cv2.rectangle(frame, (coords[0], coords[1]), (coords[2], coords[3]), (0, 140, 255), 2)
            
            # Add text label (Class Name + Confidence %)
            label = f"{cls_name} {conf:.1f}%"
            cv2.putText(frame, label, (coords[0], max(20, coords[1] - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 140, 255), 2)

        # 5. Display the resulting frame
        cv2.imshow("Model 2 Isolated Test", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_model2()