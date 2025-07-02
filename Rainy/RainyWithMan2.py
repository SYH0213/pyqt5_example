import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer

class RainDrop:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

class RainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("비 + 우산 쓴 슬픈 캐릭터 걷기")
        self.setGeometry(100, 100, 600, 400)

        # 비 생성
        self.raindrops = [RainDrop(random.randint(0, 600), random.randint(0, 400), random.randint(2, 5)) for _ in range(120)]

        # 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        self.timer.start(30)

        self.t = 0  # 애니메이션 타이머
        self.character_x = -50  # 캐릭터 시작 위치 (왼쪽 밖)
        self.character_y = self.height() // 2 + 40
        self.speed = 1.5  # 걷는 속도

    def updateScene(self):
        # 비 떨어지기
        for drop in self.raindrops:
            drop.y += drop.speed
            if drop.y > self.height():
                drop.y = 0
                drop.x = random.randint(0, self.width())

        # 캐릭터 이동
        self.character_x += self.speed
        if self.character_x > self.width() + 50:
            self.character_x = -50  # 왼쪽에서 다시 등장

        self.t += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 배경
        painter.fillRect(self.rect(), QColor(40, 40, 60))

        # 비
        painter.setPen(QColor(150, 200, 255))
        for drop in self.raindrops:
            painter.drawLine(drop.x, drop.y, drop.x, drop.y + 10)

        # 캐릭터 위치
        cx = int(self.character_x)
        cy = int(self.character_y)
        offset = int(math.sin(self.t * 0.1) * 4)  # 우산 흔들림

        # 우산
        painter.setBrush(QColor(255, 80, 80))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - 40 + offset, cy - 100, 80, 40)

        # 우산 손잡이
        painter.setPen(QColor(100, 60, 60))
        painter.drawLine(cx + offset, cy - 60, cx + offset, cy - 20)

        # 머리 (오른쪽 방향 보는 느낌 → 타원)
        painter.setBrush(QColor(255, 224, 189))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - 10, cy - 20, 25, 30)

        # 눈 (오른쪽 눈 하나만 점으로)
        painter.setPen(QPen(QColor(80, 50, 50), 3))
        painter.drawPoint(cx + 5, cy - 5)

        # 슬픈 입 (오른쪽으로 약간 기울인 아크)
        painter.setPen(QPen(QColor(80, 50, 50), 2))
        painter.drawArc(cx - 3, cy + 5, 10, 6, 0, -180 * 16)

        # 몸 (살짝 오른쪽으로 기울게)
        painter.setBrush(QColor(100, 100, 255))
        painter.setPen(Qt.NoPen)
        painter.drawRect(cx - 5, cy + 10, 15, 40)

        # 다리 (한쪽 다리만 앞으로 나가 있는 느낌)
        painter.setPen(QPen(QColor(50, 50, 50), 2))
        painter.drawLine(cx, cy + 50, cx, cy + 70)        # 오른쪽 다리
        painter.drawLine(cx - 4, cy + 50, cx - 6, cy + 68)  # 왼쪽 다리 뒤로 약간



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RainWidget()
    window.show()
    sys.exit(app.exec_())
