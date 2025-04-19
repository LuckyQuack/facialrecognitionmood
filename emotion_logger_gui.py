from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QInputDialog
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import sys
import os
import json

DATA_FILE = "emotions.json"

EMOTION_TO_SCORE = {
    "Sad": -1,
    "Neutral": 0,
    "Happy": 1,
}

class EmotionLogger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emotion Logger")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Logged Emotions:")
        self.layout.addWidget(self.label)
        
        self.emotion_list = QListWidget()
        self.layout.addWidget(self.emotion_list)
        
        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.clicked.connect(self.edit_emotion)
        self.layout.addWidget(self.edit_button)

        self.chart_button = QPushButton("Show Emotion Trend")
        self.chart_button.clicked.connect(self.show_emotion_graph)
        self.layout.addWidget(self.chart_button)
        
        self.setLayout(self.layout)
        
        # Load existing data or start fresh
        self.emotions = self.load_emotions()
        self.update_list()

    def load_emotions(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = f.read().strip()
                    if not data:
                        return []
                    return json.loads(data)
            except json.JSONDecodeError:
                return []
        return []


    def save_emotions(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.emotions, f)

    def update_list(self):
        self.emotion_list.clear()
        for timestamp, emotion in self.emotions:
            try:
                time_display = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%b %d %I:%M %p")
            except ValueError:
                time_display = timestamp  # fallback
            self.emotion_list.addItem(f"{time_display}: {emotion}")

    def add_emotion(self, emotion):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # full timestamp
        self.emotions.append((timestamp, emotion))
        self.save_emotions()
        self.update_list()

    def edit_emotion(self):
        selected = self.emotion_list.currentRow()
        if selected >= 0:
            time, emotion = self.emotions[selected]
            new_emotion, ok = QInputDialog.getText(self, "Edit Emotion", f"Edit emotion at {time}:", text=emotion)
            if ok and new_emotion:
                self.emotions[selected] = (time, new_emotion)
                self.save_emotions()
                self.update_list()

    def show_emotion_graph(self):
        import matplotlib.pyplot as plt
        from collections import defaultdict
        from datetime import datetime

        daily_scores = defaultdict(list)

        # Group scores by date
        for timestamp, emotion in self.emotions:
            try:
                # Attempt to parse full timestamp
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Fallback if timestamp only has time
                dt = datetime.now().replace(hour=int(timestamp.split(":")[0]), minute=int(timestamp.split(":")[1]))
            date_str = dt.strftime("%Y-%m-%d")
            score = EMOTION_TO_SCORE.get(emotion, 0)
            daily_scores[date_str].append(score)

        # Prepare lists for plotting
        dates = sorted(daily_scores.keys())
        avg_scores = [sum(scores) / len(scores) for scores in [daily_scores[d] for d in dates]]

        # Plotting
        plt.figure(figsize=(8, 4))
        plt.plot(dates, avg_scores, marker='o', linewidth=2, color='mediumseagreen')
        plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)

        plt.yticks([-2, -1, 0, 1, 2], ['Very Unpleasant', 'Sad', 'Neutral', 'Happy', 'Very Pleasant'])
        plt.xticks(rotation=45, fontsize=8)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.title("Average Mood per Day", fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Clean up chart borders
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.show()

def launch_gui():
    app = QApplication(sys.argv)
    window = EmotionLogger()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launch_gui()
