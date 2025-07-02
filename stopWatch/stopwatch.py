
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
from stopwatch_ui import Ui_Form

class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.time = 0
        self.is_running = False

        self.ui.btn1.clicked.connect(self.start_stopwatch)
        self.ui.btn2.clicked.connect(self.stop_reset_handler)

    def start_stopwatch(self):
        if not self.is_running:
            self.timer.start(10)  # 10ms마다 업데이트
            self.is_running = True
            self.ui.btn2.setText("Stop")

    def stop_reset_handler(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            self.ui.btn2.setText("Reset")
        else:
            self.time = 0
            self.display_time()

    def update_time(self):
        self.time += 1
        self.display_time()

    def display_time(self):
        minutes = self.time // 6000
        seconds = (self.time // 100) % 60
        milliseconds = (self.time % 100) // 10
        self.ui.label1.setText(f"{minutes:02d}:{seconds:02d}.{milliseconds}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    sys.exit(app.exec_())
