import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer

class RainDrop:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

class RainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("비 내리는 애니메이션")
        self.setGeometry(100, 100, 600, 400)

        self.raindrops = [RainDrop(random.randint(0, 600), random.randint(0, 400), random.randint(2, 6)) for _ in range(100)]

        # 타이머로 애니메이션 반복
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateRain)
        self.timer.start(30)  # 30ms 간격으로 update()

    def updateRain(self):
        for drop in self.raindrops:
            drop.y += drop.speed
            if drop.y > self.height():  # 아래로 다 떨어지면 다시 위로
                drop.y = 0
                drop.x = random.randint(0, self.width())
        self.update()  # repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(30, 30, 30))  # 어두운 배경

        painter.setPen(QColor(135, 206, 250))  # 연한 파란색 (비 색)
        for drop in self.raindrops:
            painter.drawLine(drop.x, drop.y, drop.x, drop.y + 10)  # 짧은 선으로 비 표현

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RainWidget()
    window.show()
    sys.exit(app.exec_())
