import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class StopwatchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stopwatch')
        self.is_running = False
        self.time_counter = 0

        # UI Elements
        # Time Label
        self.time_label = QLabel('00:00.0', self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont('Arial', 80))

        # Buttons
        self.start_button = QPushButton('Start', self)
        self.stop_button = QPushButton('Stop', self)
        self.reset_button = QPushButton('Reset', self)

        # Styling (based on the image)
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px;")
        self.stop_button.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; padding: 10px;")
        self.reset_button.setStyleSheet("background-color: #808080; color: white; font-size: 16px; padding: 10px;")

        # Layout
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)

        main_layout.addWidget(self.time_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Timer
        self.timer = QTimer(self)
        self.timer.setInterval(100) # Update every tenth of a second
        self.timer.timeout.connect(self.update_time)

        # Connections
        self.start_button.clicked.connect(self.start_timer)
        self.stop_button.clicked.connect(self.stop_timer)
        self.reset_button.clicked.connect(self.reset_timer)

    def start_timer(self):
        if not self.is_running:
            self.timer.start()
            self.is_running = True

    def stop_timer(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.time_counter = 0
        self.time_label.setText('00:00.0')

    def update_time(self):
        self.time_counter += 1
        minutes = self.time_counter // 600
        seconds = (self.time_counter // 10) % 60
        tenths = self.time_counter % 10
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}.{tenths}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stopwatch = StopwatchApp()
    stopwatch.resize(400, 300)
    stopwatch.show()
    sys.exit(app.exec_())
