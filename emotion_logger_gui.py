from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QInputDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
import sys
import os
import json

DATA_FILE = "emotions.json"

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
        self.chart_button.clicked.connect(self.show_emotion_chart)
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
        for time, emotion in self.emotions:
            self.emotion_list.addItem(f"{time}: {emotion}")

    def add_emotion(self, emotion):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # timestamp format
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

    def show_emotion_chart(self):
        if not self.emotions:
            return

        # Parse times and emotions
        timestamps = []
        emotion_labels = []
        for time_str, emotion in self.emotions:
            try:
                # Try parsing with time only or datetime
                if ":" in time_str and "AM" in time_str or "PM" in time_str:
                    time_obj = datetime.strptime(time_str, "%I:%M %p")
                else:
                    time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            timestamps.append(time_obj)
            emotion_labels.append(emotion)

        # Map emotions to numerical values
        unique_emotions = list(sorted(set(emotion_labels)))
        emotion_to_value = {emotion: idx for idx, emotion in enumerate(unique_emotions)}
        numeric_emotions = [emotion_to_value[e] for e in emotion_labels]

        # Clear previous chart
        if hasattr(self, 'chart_canvas'):
            self.layout.removeWidget(self.chart_canvas)
            self.chart_canvas.deleteLater()

        # Create chart
        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)
        ax.plot(timestamps, numeric_emotions, marker='o', linestyle='-')
        ax.set_yticks(list(emotion_to_value.values()))
        ax.set_yticklabels(unique_emotions)
        ax.set_title("Emotion Trend Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Emotion")
        fig.autofmt_xdate()

        self.chart_canvas = FigureCanvas(fig)
        self.layout.addWidget(self.chart_canvas)



def launch_gui():
    app = QApplication(sys.argv)
    window = EmotionLogger()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launch_gui()
