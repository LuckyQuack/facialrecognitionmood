import numpy as np
from collections import deque

class EmotionStabilizer:
    def __init__(self, window_size=10):
        self.rolling_window = deque(maxlen=window_size)
        self.desired_emotions = ["Happy", "Neutral", "Sad"]

    def get_stable_emotion(self, detected_emotion):
        """Returns the most common emotion from the rolling window."""
        self.rolling_window.append(detected_emotion)

        weights = np.linspace(0.5, 1, len(self.rolling_window))  # More weight to recent emotions
        emotion_counts = {emotion: 0 for emotion in self.desired_emotions}

        for i, emotion in enumerate(self.rolling_window):
            weight = weights[i]
            if emotion == "Sad":
                weight *= 1.4  # Boost Sad detection  
            emotion_counts[emotion] += weight

        return max(emotion_counts, key=emotion_counts.get)  # Most weighted emotion