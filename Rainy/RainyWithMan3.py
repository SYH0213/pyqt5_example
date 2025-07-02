import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer

class RainDrop:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

class RainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("비 오는 날 슬픈 캐릭터")
        self.setGeometry(100, 100, 600, 400)

        self.raindrops = [RainDrop(random.randint(0, 600), random.randint(0, 400), random.randint(2, 5)) for _ in range(120)]

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        self.timer.start(30)

        self.t = 0
        self.character_x = -50
        self.character_y = self.height() // 2 + 40
        self.speed = 1.5

    def updateScene(self):
        for drop in self.raindrops:
            drop.y += drop.speed
            if drop.y > self.height():
                drop.y = 0
                drop.x = random.randint(0, self.width())

        self.character_x += self.speed
        if self.character_x > self.width() + 50:
            self.character_x = -50

        self.t += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(40, 40, 60))

        # 비
        painter.setPen(QColor(150, 200, 255))
        for drop in self.raindrops:
            painter.drawLine(drop.x, drop.y, drop.x, drop.y + 10)

        cx = int(self.character_x)
        breathing_offset_y = int(math.sin(self.t * 0.08) * 2)
        cy = int(self.character_y + breathing_offset_y)
        umbrella_offset_y = int(math.sin(self.t * 0.1) * 2)

        # ☂ 우산: 반원 + 살대 + 봉
        arc_center_x = cx
        arc_center_y = cy - 50 + umbrella_offset_y
        radius = 50

        painter.setBrush(QColor(255, 80, 80))
        painter.setPen(QPen(QColor(120, 30, 30), 2))
        painter.drawArc(arc_center_x - radius, arc_center_y - radius, radius * 2, radius * 2, 0, 180 * 16)

        # 우산 살대들 (정수로 변환 추가)
        painter.setPen(QPen(QColor(100, 40, 40), 1))
        for angle in range(15, 165, 30):
            rad = math.radians(angle)
            x = int(arc_center_x + radius * math.cos(rad))
            y = int(arc_center_y + radius * math.sin(rad))
            painter.drawLine(arc_center_x, arc_center_y, x, y)

        # 우산 봉
        painter.setPen(QPen(QColor(100, 60, 60), 3))
        painter.drawLine(arc_center_x, arc_center_y, arc_center_x, cy - 20)

        # 👤 머리
        painter.setBrush(QColor(255, 224, 189))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - 10, cy - 20, 25, 30)

        # 👁 눈 + 눈썹
        painter.setPen(QPen(QColor(50, 30, 30), 3))
        painter.drawPoint(cx + 5, cy - 5)
        painter.setPen(QPen(QColor(50, 30, 30), 2))
        painter.drawLine(cx + 3, cy - 10, cx + 8, cy - 12)

        # 🙁 입 (슬픔)
        painter.setPen(QPen(QColor(80, 50, 50), 2))
        painter.drawArc(cx - 3, cy + 5, 10, 6, 0, -180 * 16)

        # 👕 몸통
        painter.setBrush(QColor(100, 100, 255))
        painter.setPen(Qt.NoPen)
        painter.drawRect(cx - 5, cy + 10, 15, 40)

        # 🦵 다리 (중앙 기준 좌우로 정확히 나뉨)
        leg_offset = int(math.sin(self.t * 0.2) * 5)
        painter.setPen(QPen(QColor(50, 50, 50), 2))
        painter.drawLine(cx - 6, cy + 50, cx - 6 + leg_offset, cy + 70)
        painter.drawLine(cx + 6, cy + 50, cx + 6 - leg_offset, cy + 70)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RainWidget()
    window.show()
    sys.exit(app.exec_())
