import cv2
import numpy as np
import time
from collections import Counter
from detector import FaceDetector
from emotion_model import predict_emotion
from stabilizer import EmotionStabilizer
from datetime import datetime

# Initialize modules
face_detector = FaceDetector()
stabilizer = EmotionStabilizer()
cap = cv2.VideoCapture(0)

neutral_baseline = None  # Stores first detected neutral state of eyebrows for reference
emotions_during_session = []

# Duration limit
DETECTION_DURATION = 10  # seconds
start_time = time.time()

while cap.isOpened():
    if time.time() - start_time > DETECTION_DURATION:
        break

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

            face_roi = frame[y:y+height, x:x+width]
            face_roi = cv2.resize(face_roi, (48, 48))
            face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

            detected_emotion = predict_emotion(face_roi)

            stable_emotion = stabilizer.get_stable_emotion(detected_emotion)
            emotions_during_session.append(stable_emotion)

            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            cv2.putText(frame, stable_emotion, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# Log the most frequent emotion from session
if emotions_during_session:
    most_common_emotion = Counter(emotions_during_session).most_common(1)[0][0]

    # Import the logger GUI and add emotion
    from emotion_logger_gui import EmotionLogger
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    emotion_logger = EmotionLogger()
    emotion_logger.add_emotion(stable_emotion)
    emotion_logger.show()
    sys.exit(app.exec())

#what to work on
#fix neutral strength ; neutral shows too much