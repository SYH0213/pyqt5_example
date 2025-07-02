import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter, QPen

class GeneratedStopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Generated Jjolaman Stopwatch')
        self.is_running = False
        self.time_counter = 0

        # --- Animation Setup ---
        self.animation_label = QLabel(self)
        self.animation_label.setAlignment(Qt.AlignCenter)
        self.animation_frames = self.create_animation_frames()
        self.current_frame = 0
        if self.animation_frames:
            self.animation_label.setPixmap(self.animation_frames[0])

        # --- UI Elements ---
        self.time_label = QLabel('00:00.0', self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont('Arial', 80))

        self.start_button = QPushButton('Start', self)
        self.stop_button = QPushButton('Stop', self)
        self.reset_button = QPushButton('Reset', self)

        # Styling
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px;")
        self.stop_button.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; padding: 10px;")
        self.reset_button.setStyleSheet("background-color: #808080; color: white; font-size: 16px; padding: 10px;")

        # --- Layout ---
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)

        main_layout.addWidget(self.animation_label)
        main_layout.addWidget(self.time_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # --- Timers ---
        self.stopwatch_timer = QTimer(self)
        self.stopwatch_timer.setInterval(100)
        self.stopwatch_timer.timeout.connect(self.update_time)

        self.animation_timer = QTimer(self)
        self.animation_timer.setInterval(150)
        self.animation_timer.timeout.connect(self.update_animation)

        # --- Connections ---
        self.start_button.clicked.connect(self.start_all)
        self.stop_button.clicked.connect(self.stop_all)
        self.reset_button.clicked.connect(self.reset_all)

    def create_animation_frames(self):
        frames = []
        frame_size = (100, 120)
        poses = [
            # Frame 1: Left leg forward
            {'head': (40, 10, 20, 20), 'torso': (50, 30, 50, 70), 'left_arm': (50, 45, 30, 65), 'right_arm': (50, 45, 70, 65), 'left_leg': (50, 70, 30, 100), 'right_leg': (50, 70, 70, 100)},
            # Frame 2: Legs together
            {'head': (40, 10, 20, 20), 'torso': (50, 30, 50, 70), 'left_arm': (50, 45, 40, 60), 'right_arm': (50, 45, 60, 60), 'left_leg': (50, 70, 45, 100), 'right_leg': (50, 70, 55, 100)},
            # Frame 3: Right leg forward
            {'head': (40, 10, 20, 20), 'torso': (50, 30, 50, 70), 'left_arm': (50, 45, 70, 65), 'right_arm': (50, 45, 30, 65), 'left_leg': (50, 70, 70, 100), 'right_leg': (50, 70, 30, 100)},
            # Frame 4: Legs together (same as frame 2)
            {'head': (40, 10, 20, 20), 'torso': (50, 30, 50, 70), 'left_arm': (50, 45, 40, 60), 'right_arm': (50, 45, 60, 60), 'left_leg': (50, 70, 45, 100), 'right_leg': (50, 70, 55, 100)},
        ]

        for pose in poses:
            pixmap = QPixmap(frame_size[0], frame_size[1])
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            pen = QPen(Qt.black, 3)
            painter.setPen(pen)
            
            painter.drawEllipse(*pose['head'])
            painter.drawLine(*pose['torso'])
            painter.drawLine(*pose['left_arm'])
            painter.drawLine(*pose['right_arm'])
            painter.drawLine(*pose['left_leg'])
            painter.drawLine(*pose['right_leg'])
            
            painter.end()
            frames.append(pixmap)
        return frames

    def start_all(self):
        if not self.is_running:
            self.stopwatch_timer.start()
            self.animation_timer.start()
            self.is_running = True

    def stop_all(self):
        if self.is_running:
            self.stopwatch_timer.stop()
            self.animation_timer.stop()
            self.is_running = False

    def reset_all(self):
        self.stopwatch_timer.stop()
        self.animation_timer.stop()
        self.is_running = False
        self.time_counter = 0
        self.current_frame = 0
        self.time_label.setText('00:00.0')
        if self.animation_frames:
            self.animation_label.setPixmap(self.animation_frames[0])

    def update_time(self):
        self.time_counter += 1
        minutes = self.time_counter // 600
        seconds = (self.time_counter // 10) % 60
        tenths = self.time_counter % 10
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}.{tenths}")

    def update_animation(self):
        self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
        self.animation_label.setPixmap(self.animation_frames[self.current_frame])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stopwatch = GeneratedStopwatch()
    stopwatch.resize(400, 450)
    stopwatch.show()
    sys.exit(app.exec_())
