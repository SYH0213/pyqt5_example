import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QTimer

class RainDrop:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

class RainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("비 + 사람 애니메이션")
        self.setGeometry(100, 100, 600, 400)

        self.raindrops = [RainDrop(random.randint(0, 600), random.randint(0, 400), random.randint(2, 5)) for _ in range(120)]

        # 애니메이션 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateRain)
        self.timer.start(30)

        self.t = 0  # 우산 흔들림을 위한 시간 변수

    def updateRain(self):
        for drop in self.raindrops:
            drop.y += drop.speed
            if drop.y > self.height():
                drop.y = 0
                drop.x = random.randint(0, self.width())
        self.t += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(40, 40, 60))  # 밤색 배경

        # 비 그리기
        painter.setPen(QColor(150, 200, 255))
        for drop in self.raindrops:
            painter.drawLine(drop.x, drop.y, drop.x, drop.y + 10)

        # 사람+우산 그리기 (중앙)
        cx = self.width() // 2
        cy = self.height() // 2 + 40

        # 우산 흔들림 애니메이션 (좌우로 살짝 흔들리기)
        offset = int(math.sin(self.t * 0.1) * 5)

        # 우산
        painter.setBrush(QColor(255, 80, 80))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - 40 + offset, cy - 100, 80, 40)

        # 손잡이
        painter.setPen(QColor(100, 60, 60))
        painter.drawLine(cx + offset, cy - 60, cx + offset, cy - 20)

        # 머리
        painter.setBrush(QColor(255, 224, 189))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - 15, cy - 20, 30, 30)

        # 몸
        painter.setBrush(QColor(100, 100, 255))
        painter.drawRect(cx - 10, cy + 10, 20, 40)

        # 다리
        painter.setPen(QColor(50, 50, 50))
        painter.drawLine(cx - 5, cy + 50, cx - 5, cy + 70)
        painter.drawLine(cx + 5, cy + 50, cx + 5, cy + 70)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RainWidget()
    window.show()
    sys.exit(app.exec_())
