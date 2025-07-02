import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
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
            drop.x += 0.5  # 살짝 오른쪽으로 이동해서 비스듬히 표현
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

        # 흐린 배경 처리
        painter.fillRect(self.rect(), QColor(30, 30, 50, 200))

        # 비 (살짝 대각선 방향)
        painter.setPen(QColor(150, 200, 255, 150))
        for drop in self.raindrops:
            painter.drawLine(int(drop.x), int(drop.y), int(drop.x + 2), int(drop.y + 10))

        cx = int(self.character_x)
        breathing_offset_y = int(math.sin(self.t * 0.08) * 2)
        cy = int(self.character_y + breathing_offset_y)
        umbrella_offset_y = int(math.sin(self.t * 0.1) * 2)

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

        # 💪 팔 (오른팔 앞으로 뻗음)
        painter.setPen(QPen(QColor(255, 224, 189), 4))
        hand_x = cx + 15
        hand_y = cy + 25
        painter.drawLine(cx + 2, cy + 20, hand_x, hand_y)

        # ☂ 우산 봉 (팔 끝에서 기울인 방향으로)
        pole_top_x = hand_x - 10
        pole_top_y = hand_y - 30
        painter.setPen(QPen(QColor(100, 60, 60), 3))
        painter.drawLine(hand_x, hand_y, pole_top_x, pole_top_y)

        # ☂ 반타원형 우산 (기울어진 상태, 봉 윗부분 기준으로 위치 조정)
        painter.save()
        painter.translate(pole_top_x, pole_top_y + umbrella_offset_y)
        painter.rotate(-20)  # 왼쪽으로 기울이기
        painter.setBrush(QColor(255, 80, 80))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-45, -40, 90, 40)
        painter.restore()

        # 🦵 다리 (중앙 기준 좌우)
        leg_offset = int(math.sin(self.t * 0.2) * 5)
        painter.setPen(QPen(QColor(50, 50, 50), 2))
        painter.drawLine(cx - 6, cy + 50, cx - 6 + leg_offset, cy + 70)
        painter.drawLine(cx + 6, cy + 50, cx + 6 - leg_offset, cy + 70)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RainWidget()
    window.show()
    sys.exit(app.exec_())
