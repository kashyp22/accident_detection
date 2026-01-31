# import cv2
# import torch
# from transformers import DetrForObjectDetection, DetrFeatureExtractor
#
# # 1) Load the model
# model_name = "hilmantm/detr-traffic-accident-detection"
# feature_extractor = DetrFeatureExtractor.from_pretrained(model_name)
# model = DetrForObjectDetection.from_pretrained(model_name)
# model.eval()
#
# # 2) Open the webcam
# cap = cv2.VideoCapture(0)  # 0 for default camera
#
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     # Convert frame to RGB and prepare inputs
#     image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     inputs = feature_extractor(images=image_rgb, return_tensors="pt")
#
#     with torch.no_grad():
#         outputs = model(**inputs)
#
#     # `outputs` contains boxes and labels + scores
#     target_sizes = torch.tensor([image_rgb.shape[:2]])
#     results = feature_extractor.post_process_object_detection(
#         outputs, target_sizes=target_sizes, threshold=0.5
#     )[0]
#
#     # Draw boxes on the frame
#     for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
#         score = round(score.item(), 3)
#         label_id = label.item()
#         x1, y1, x2, y2 = map(int, box.tolist())
#
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(frame, f"{model.config.id2label[label_id]} {score}",
#                     (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
#
#     cv2.imshow("Accident Detection", frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

import cv2
import torch
from transformers import DetrForObjectDetection, DetrImageProcessor
import time

# 1) Load the model
model_name = "hilmantm/detr-traffic-accident-detection"
processor = DetrImageProcessor.from_pretrained(model_name)
model = DetrForObjectDetection.from_pretrained(model_name)
model.eval()

# 2) Open the webcam
cap = cv2.VideoCapture(0)  # 0 for default camera

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to RGB and prepare inputs
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    inputs = processor(images=image_rgb, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    # Post-process the outputs
    target_sizes = torch.tensor([image_rgb.shape[:2]])
    results = processor.post_process_object_detection(
        outputs, target_sizes=target_sizes, threshold=0.5
    )[0]

    # Draw boxes on the frame
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        score = round(score.item(), 3)
        label_id = label.item()
        x1, y1, x2, y2 = map(int, box.tolist())

        # Get label name
        label_name = model.config.id2label.get(label_id, f"Class {label_id}")
        if label_name == "accident":
        # Draw rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label background
            text = f"{label_name} {score}"
            (text_width, text_height), baseline = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(frame, (x1, y1 - text_height - 10),
                          (x1 + text_width, y1), (0, 255, 0), -1)

            # Draw text
            cv2.putText(frame, text, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            # filename = f"accident_detection_{int(time.time())}.jpg"
            # cv2.imwrite(filename, frame)
            # print(f"Frame saved as {filename}")

            import cv2
            import requests
            import time
            from io import BytesIO

            url = "http://localhost:8000/myapp/accident_detection/"

            # Encode frame as JPEG in memory
            success, encoded_img = cv2.imencode(".jpg", frame)

            if success:
                image_bytes = encoded_img.tobytes()

                files = {
                    "image": ("accident.jpg", image_bytes, "image/jpeg")
                }

                data = {
                    "uid": "1"
                }

                response = requests.post(url, files=files, data=data)

                print(response.status_code)
                print(response.text)

    # Display FPS (optional)
    cv2.putText(frame, "Press 'q' to quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Accident Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Detection stopped")