import cv2
import mediapipe as mp

class FaceDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)

        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

    def detect_faces(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_results = self.face_detection.process(rgb_frame)
        mesh_results = self.face_mesh.process(rgb_frame)

        return face_results.detections if face_results.detections else None, mesh_results.multi_face_landmarks if mesh_results.multi_face_landmarks else None
