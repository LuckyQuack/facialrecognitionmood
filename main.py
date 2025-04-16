import cv2
import numpy as np
from detector import FaceDetector
from emotion_model import predict_emotion
from stabilizer import EmotionStabilizer

# Initialize modules
face_detector = FaceDetector()
stabilizer = EmotionStabilizer()
cap = cv2.VideoCapture(0)

neutral_baseline = None  # Stores first detected neutral state of eyebrows for reference

# Get eyebrow ratio for neutral baseline
def get_eyebrow_height_ratio(landmarks, img_h, img_w):
    """
    Measures eyebrow height relative to the eyes.
    Lower height → possible neutral state misclassification.
    """
    global neutral_baseline

    left_brow = np.array([(landmarks[70].x * img_w, landmarks[70].y * img_h)])
    right_brow = np.array([(landmarks[295].x * img_w, landmarks[295].y * img_h)])
    
    left_eye = np.array([(landmarks[159].x * img_w, landmarks[159].y * img_h)])
    right_eye = np.array([(landmarks[386].x * img_w, landmarks[386].y * img_h)])
    
    left_ratio = abs(left_brow[0][1] - left_eye[0][1])
    right_ratio = abs(right_brow[0][1] - right_eye[0][1])
    
    current_ratio = (left_ratio + right_ratio) / 2  # Average for both eyebrows

    if neutral_baseline is None:
        neutral_baseline = current_ratio

    return current_ratio

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img_h, img_w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face & facial landmarks
    face_results, mesh_results = face_detector.detect_faces(rgb_frame)

    if face_results and mesh_results:
        for detection, landmarks in zip(face_results, mesh_results):
            bbox = detection.location_data.relative_bounding_box
            x, y, width, height = int(bbox.xmin * img_w), int(bbox.ymin * img_h), int(bbox.width * img_w), int(bbox.height * img_h)

            # Extract face ROI
            face_roi = frame[y:y+height, x:x+width]
            face_roi = cv2.resize(face_roi, (48, 48))
            face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

            # Predict emotion
            detected_emotion = predict_emotion(face_roi)

            # Adjust emotion using eyebrow data
            eyebrow_ratio = get_eyebrow_height_ratio(landmarks.landmark, img_h, img_w)
            if neutral_baseline is not None and abs(eyebrow_ratio - neutral_baseline) < 3:
                detected_emotion = "Neutral"
            elif detected_emotion == "Sad" and abs(eyebrow_ratio - neutral_baseline) < 5:
                detected_emotion = "Neutral"

            stable_emotion = stabilizer.get_stable_emotion(detected_emotion)

            # Draw bounding box & emotion label
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            cv2.putText(frame, stable_emotion, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
