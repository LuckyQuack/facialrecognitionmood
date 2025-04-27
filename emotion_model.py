import numpy as np
from tensorflow.keras.models import load_model

# Load pre-trained model
model = load_model("models/face_model.h5")

# Emotion labels based on model output
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]
desired_emotions = ["Happy", "Neutral", "Sad"]

def map_emotion(prediction):
    """Remaps model output to desired emotions (happy, sad, neutral) with adjusted thresholds."""
    probabilities = prediction[0]
    
    # Get the top two emotions and their probabilities
    indices = np.argsort(probabilities)[-2:]
    top_emotion = emotion_labels[indices[1]]
    top_prob = probabilities[indices[1]]
    second_emotion = emotion_labels[indices[0]]
    second_prob = probabilities[indices[0]]
    
    # Adjust neutral detection threshold
    if top_emotion == "Neutral" and top_prob < 0.3:
        # If confidence in neutral is low, consider the second highest emotion
        if second_emotion == "Happy" and second_prob > 0.2:
            return "Happy"
        elif second_emotion in ["Sad", "Angry", "Disgust", "Fear"] and second_prob > 0.2:
            return "Sad"
    
    # Enhanced mapping for exaggerated expressions
    if top_emotion == "Surprise" and top_prob > 0.4:
        return "Happy"
    if top_emotion in ["Angry", "Disgust", "Fear"] and top_prob > 0.4:
        return "Sad"
    if top_emotion == "Happy" and top_prob > 0.3: 
        return "Happy"
    if top_emotion == "Sad" and top_prob > 0.3:    
        return "Sad"
        
    # Default mappings
    if top_emotion in ["Surprise"]:
        return "Happy"
    if top_emotion in ["Angry", "Disgust", "Fear"]:
        return "Sad"

    return top_emotion

def predict_emotion(face_roi):
    """Preprocesses input & predicts emotion."""
    face_roi = np.expand_dims(face_roi, axis=(0, -1))
    prediction = model.predict(face_roi)
    return map_emotion(prediction)