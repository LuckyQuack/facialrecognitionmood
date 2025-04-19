import numpy as np
from tensorflow.keras.models import load_model

# Load pre-trained model
model = load_model("models/face_model.h5")

# Emotion labels based on model output
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]
desired_emotions = ["Happy", "Neutral", "Sad"]

def map_emotion(prediction):
    """Remaps model output to desired emotions (happy, sad, neutral)."""
    probabilities = prediction[0]
    dominant_idx = np.argmax(probabilities)
    dominant_emotion = emotion_labels[dominant_idx]

    if dominant_emotion in ["Surprise"]:
        return "Happy"
    if dominant_emotion in ["Angry", "Disgust", "Fear"]:
        return "Sad"

    return dominant_emotion  

def predict_emotion(face_roi):
    """Preprocesses input & predicts emotion."""
    face_roi = np.expand_dims(face_roi, axis=(0, -1))
    prediction = model.predict(face_roi)
    return map_emotion(prediction)

#visualize data
#save previous data
#neutral is too strong but we must focus on accuracy so maybe large change from neutral state should affect it