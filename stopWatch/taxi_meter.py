import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter, QPen, QColor

class TaxiMeter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('말 달리는 택시 미터기')
        self.is_running = False
        self.time_counter = 0
        self.base_fare = 3800
        self.current_fare = self.base_fare

        # --- UI Styling ---
        self.setStyleSheet("background-color: #2C3E50;")

        # --- Horse Animation ---
        self.animation_label = QLabel(self)
        self.animation_label.setAlignment(Qt.AlignCenter)
        self.animation_frames = self.create_horse_frames()
        self.current_frame = 0
        if self.animation_frames:
            self.animation_label.setPixmap(self.animation_frames[0])

        # --- Meter Display ---
        meter_frame = QFrame(self)
        meter_frame.setStyleSheet("background-color: #1A242F; border-radius: 5px;")
        meter_layout = QHBoxLayout(meter_frame)

        fare_title_label = QLabel('요금', self)
        fare_title_label.setFont(QFont('Courier New', 24, QFont.Bold))
        fare_title_label.setStyleSheet("color: white;")

        self.fare_label = QLabel(f"{self.base_fare:,}", self)
        self.fare_label.setFont(QFont('Courier New', 48, QFont.Bold))
        self.fare_label.setStyleSheet("color: #E74C3C;")
        self.fare_label.setAlignment(Qt.AlignRight)

        won_label = QLabel('원', self)
        won_label.setFont(QFont('Courier New', 24, QFont.Bold))
        won_label.setStyleSheet("color: white;")

        meter_layout.addWidget(fare_title_label)
        meter_layout.addStretch(1)
        meter_layout.addWidget(self.fare_label)
        meter_layout.addWidget(won_label)

        # --- Buttons ---
        self.start_button = QPushButton('Start', self)
        self.stop_button = QPushButton('Stop', self)
        self.reset_button = QPushButton('Reset', self)
        button_style = """
            QPushButton {
                background-color: #34495E; color: white; 
                font-size: 16px; padding: 10px; border-radius: 5px;
            }
            QPushButton:hover {background-color: #4E6D8C;}
        """
        self.start_button.setStyleSheet(button_style)
        self.stop_button.setStyleSheet(button_style)
        self.reset_button.setStyleSheet(button_style)

        # --- Layout ---
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)

        main_layout.addWidget(self.animation_label)
        main_layout.addWidget(meter_frame)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # --- Timers ---
        self.fare_timer = QTimer(self)
        self.fare_timer.setInterval(100) # Fare update interval
        self.fare_timer.timeout.connect(self.update_fare)

        self.animation_timer = QTimer(self)
        self.animation_timer.setInterval(150) # Animation speed
        self.animation_timer.timeout.connect(self.update_animation)

        # --- Connections ---
        self.start_button.clicked.connect(self.start_meter)
        self.stop_button.clicked.connect(self.stop_meter)
        self.reset_button.clicked.connect(self.reset_meter)

    def create_horse_frames(self):
        from PyQt5.QtGui import QPolygonF
        from PyQt5.QtCore import QPointF
        frames = []
        frame_size = (220, 120)
        
        # Detailed 4-stage gallop animation
        poses = [
            # 1. Collection (all legs under body)
            {'body': [QPointF(60, 50), QPointF(140, 45), QPointF(150, 65), QPointF(70, 70)], 'neck': [QPointF(140, 45), QPointF(160, 35)], 'head': (155, 20, 20, 20), 'tail': [QPointF(60, 50), QPointF(40, 40)], 'front_legs': [(130, 60, 120, 80), (120, 80, 115, 100)], 'back_legs': [(80, 65, 90, 85), (90, 85, 95, 105)]},
            # 2. Push-off (hind legs extend)
            {'body': [QPointF(50, 55), QPointF(130, 50), QPointF(140, 70), QPointF(60, 75)], 'neck': [QPointF(130, 50), QPointF(150, 40)], 'head': (145, 25, 20, 20), 'tail': [QPointF(50, 55), QPointF(30, 45)], 'front_legs': [(120, 65, 110, 85), (110, 85, 105, 105)], 'back_legs': [(70, 70, 50, 90), (50, 90, 40, 110)]},
            # 3. Flight (all legs in the air)
            {'body': [QPointF(40, 60), QPointF(120, 55), QPointF(130, 75), QPointF(50, 80)], 'neck': [QPointF(120, 55), QPointF(140, 45)], 'head': (135, 30, 20, 20), 'tail': [QPointF(40, 60), QPointF(20, 50)], 'front_legs': [(110, 70, 90, 80), (90, 80, 80, 100)], 'back_legs': [(60, 75, 40, 85), (40, 85, 30, 105)]},
            # 4. Landing (front legs extend forward)
            {'body': [QPointF(55, 50), QPointF(135, 45), QPointF(145, 65), QPointF(65, 70)], 'neck': [QPointF(135, 45), QPointF(155, 35)], 'head': (150, 20, 20, 20), 'tail': [QPointF(55, 50), QPointF(35, 40)], 'front_legs': [(125, 60, 140, 80), (140, 80, 150, 100)], 'back_legs': [(75, 65, 85, 85), (85, 85, 90, 105)]},
        ]

        for pose in poses:
            pixmap = QPixmap(frame_size[0], frame_size[1])
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            pen = QPen(QColor("#ECF0F1"), 8, cap=Qt.RoundCap, join=Qt.RoundJoin)
            painter.setPen(pen)

            # Draw body and head
            painter.drawPolygon(QPolygonF(pose['body']))
            painter.drawLine(*pose['neck'])
            painter.drawEllipse(*pose['head'])
            
            # Draw tail
            painter.drawLine(*pose['tail'])

            # Draw legs
            for leg_part in ['front_legs', 'back_legs']:
                for line in pose[leg_part]:
                    painter.drawLine(*line)
            
            painter.end()
            frames.append(pixmap)
        return frames

    def start_meter(self):
        if not self.is_running:
            self.fare_timer.start()
            self.animation_timer.start()
            self.is_running = True

    def stop_meter(self):
        if self.is_running:
            self.fare_timer.stop()
            self.animation_timer.stop()
            self.is_running = False

    def reset_meter(self):
        self.stop_meter()
        self.time_counter = 0
        self.current_fare = self.base_fare
        self.fare_label.setText(f"{self.current_fare:,}")
        self.current_frame = 0
        if self.animation_frames:
            self.animation_label.setPixmap(self.animation_frames[0])

    def update_fare(self):
        self.time_counter += 1
        # Fare increases by 100 won every 1.5 seconds
        if self.time_counter % 15 == 0:
            self.current_fare += 100
            self.fare_label.setText(f"{self.current_fare:,}")

    def update_animation(self):
        self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
        self.animation_label.setPixmap(self.animation_frames[self.current_frame])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    meter = TaxiMeter()
    meter.resize(450, 400)
    meter.show()
    sys.exit(app.exec_())
