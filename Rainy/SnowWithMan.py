import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPolygon
from PyQt5.QtCore import Qt, QTimer, QPoint

class SnowFlake:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

class SnowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("눈 오는 날 슬픈 캐릭터")
        self.setGeometry(100, 100, 600, 400)

        self.snowflakes = [SnowFlake(random.randint(0, 600), random.randint(0, 400), random.uniform(0.5, 1.5)) for _ in range(120)]
        self.tree_positions = [(x, random.randint(160, 240), random.randint(1, 3)) for x in range(0, 620, 60)]

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        self.timer.start(30)

        self.t = 0
        self.character_x = -50
        self.character_y = self.height() // 2 + 40
        self.speed = 1.2
        self.pause_timer = 0

    def updateScene(self):
        for flake in self.snowflakes:
            flake.y += flake.speed
            if flake.y > self.height():
                flake.y = 0
                flake.x = random.randint(0, self.width())

        center_x = self.width() // 2
        if abs(self.character_x - center_x) < 2 and self.pause_timer < 90:
            self.pause_timer += 1
        elif self.pause_timer >= 90:
            self.character_x += self.speed
        else:
            self.character_x += self.speed

        if self.character_x > self.width() + 50:
            self.character_x = -50
            self.pause_timer = 0

        self.t += 1
        self.update()

    def drawTree(self, painter, x, y, scale=1):
        painter.setBrush(QColor(60, 30, 10))
        painter.drawRect(x, y, 10 * scale, 50 * scale)

        painter.setBrush(QColor(20, 80, 30))
        for i in range(3):
            top = QPoint(x + 5 * scale, y - (i * 20 + 10) * scale)
            left = QPoint(x - 20 * scale + 5, y - (i * 20 - 10) * scale)
            right = QPoint(x + 30 * scale - 5, y - (i * 20 - 10) * scale)
            triangle = QPolygon([top, left, right])
            painter.drawPolygon(triangle)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(30, 30, 50, 220))

        # 소나무 스타일 나무 그리기
        for x, y, scale in sorted(self.tree_positions, key=lambda t: t[2]):
            self.drawTree(painter, x, y, scale)

        # 눈은 나무 위에 떨어짐
        painter.setPen(QColor(255, 255, 255, 200))
        for flake in self.snowflakes:
            painter.drawEllipse(int(flake.x), int(flake.y), 2, 2)

        cx = int(self.character_x)
        breathing_offset_y = int(math.sin(self.t * 0.08) * 2)
        cy = int(self.character_y + breathing_offset_y)
        umbrella_offset_y = int(math.sin(self.t * 0.1) * 2)

        painter.setBrush(QColor(255, 224, 189))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - 10, cy - 20, 25, 30)

        painter.setPen(QPen(QColor(50, 30, 30), 3))
        painter.drawPoint(cx + 5, cy - 5)
        painter.setPen(QPen(QColor(50, 30, 30), 2))
        painter.drawLine(cx + 3, cy - 10, cx + 8, cy - 12)

        painter.setPen(QPen(QColor(80, 50, 50), 2))
        painter.drawArc(cx - 3, cy + 5, 10, 6, 0, -180 * 16)

        painter.setBrush(QColor(100, 100, 255))
        painter.setPen(Qt.NoPen)
        painter.drawRect(cx - 5, cy + 10, 15, 40)

        painter.setPen(QPen(QColor(255, 224, 189), 4))
        hand_x = cx + 15
        hand_y = cy + 25
        painter.drawLine(cx + 2, cy + 20, hand_x, hand_y)

        pole_top_x = hand_x - 10
        pole_top_y = hand_y - 30
        painter.setPen(QPen(QColor(100, 60, 60), 3))
        painter.drawLine(hand_x, hand_y, pole_top_x, pole_top_y)

        painter.save()
        painter.translate(pole_top_x, pole_top_y + umbrella_offset_y)
        painter.rotate(-20)
        painter.setBrush(QColor(255, 80, 80))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-45, -40, 90, 40)
        painter.setBrush(QColor(80, 30, 30))
        painter.drawEllipse(-3, -45, 6, 6)
        painter.restore()

        if abs(self.character_x - self.width() // 2) < 2 and self.pause_timer < 90:
            painter.setBrush(QColor(255, 255, 255, 120))
            mouth_x = cx + 8
            mouth_y = cy + 10
            radius = 10 + int(math.sin(self.t * 0.3) * 2)
            painter.drawEllipse(mouth_x, mouth_y, radius, radius // 2)

        leg_offset = int(math.sin(self.t * 0.2) * 5)
        painter.setPen(QPen(QColor(50, 50, 50), 2))
        painter.drawLine(cx - 6, cy + 50, cx - 6 + leg_offset, cy + 70)
        painter.drawLine(cx + 6, cy + 50, cx + 6 - leg_offset, cy + 70)

        ground_y = self.character_y + 80
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(80, 80, 80))
        painter.drawRect(0, ground_y, self.width(), self.height() - ground_y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnowWidget()
    window.show()
    sys.exit(app.exec_())
