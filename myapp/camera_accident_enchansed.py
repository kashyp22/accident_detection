import cv2
import torch
from transformers import DetrForObjectDetection, DetrImageProcessor
from PIL import Image
import time

# Configuration
MODEL_NAME = "hilmantm/detr-traffic-accident-detection"
CONFIDENCE_THRESHOLD = 0.5
CAMERA_INDEX = 0

# Colors for different classes (BGR format)
COLORS = {
    'accident': (0, 0, 255),  # Red
    'fire': (0, 165, 255),  # Orange
    'normal': (0, 255, 0),  # Green
}


def load_model():
    """Load the DETR model and processor"""
    print("Loading model...")
    try:
        processor = DetrImageProcessor.from_pretrained(MODEL_NAME)
        model = DetrForObjectDetection.from_pretrained(MODEL_NAME)
        model.eval()

        # Move to GPU if available
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        print(f"Model loaded successfully on {device}")

        return processor, model, device
    except Exception as e:
        print(f"Error loading model: {e}")
        exit(1)


def detect_accidents(frame, processor, model, device):
    """Run accident detection on a frame"""
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Prepare inputs
    inputs = processor(images=image_rgb, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Run inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Post-process
    target_sizes = torch.tensor([image_rgb.shape[:2]]).to(device)
    results = processor.post_process_object_detection(
        outputs, target_sizes=target_sizes, threshold=CONFIDENCE_THRESHOLD
    )[0]

    return results


def draw_detections(frame, results, model):
    """Draw bounding boxes and labels on frame"""
    detections = []

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        score_val = round(score.item(), 3)
        label_id = label.item()
        x1, y1, x2, y2 = map(int, box.tolist())

        # Get label name
        label_name = model.config.id2label.get(label_id, f"Class {label_id}")

        # Choose color based on detection
        color = COLORS.get(label_name.lower(), (0, 255, 0))

        # Draw rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

        # Prepare text
        text = f"{label_name}: {score_val}"

        # Draw text background
        (text_width, text_height), baseline = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
        )
        cv2.rectangle(frame, (x1, y1 - text_height - 10),
                      (x1 + text_width + 5, y1), color, -1)

        # Draw text
        cv2.putText(frame, text, (x1 + 2, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        detections.append({
            'label': label_name,
            'confidence': score_val,
            'bbox': (x1, y1, x2, y2)
        })

    return frame, detections


def main():
    # Load model
    processor, model, device = load_model()

    # Open webcam
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print(f"Error: Could not open camera {CAMERA_INDEX}")
        return

    # Set camera resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("\n=== Accident Detection Started ===")
    print("Press 'q' to quit")
    print("Press 's' to save current frame")
    print("==================================\n")

    frame_count = 0
    fps = 0
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame_count += 1

        # Process every frame (you can skip frames for better performance)
        if frame_count % 1 == 0:  # Process every frame
            try:
                # Run detection
                results = detect_accidents(frame, processor, model, device)

                # Draw detections
                frame, detections = draw_detections(frame, results, model)

                # Print detections to console
                if detections:
                    print(f"Frame {frame_count}: Detected {len(detections)} object(s)")
                    for det in detections:
                        print(f"  - {det['label']}: {det['confidence']}")

            except Exception as e:
                print(f"Error during detection: {e}")

        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time

        # Display FPS and info
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to quit | 's' to save", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Show frame
        cv2.imshow("Traffic Accident Detection", frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f"accident_detection_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Frame saved as {filename}")

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\n=== Detection Stopped ===")


if __name__ == "__main__":
    main()