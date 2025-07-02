import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QRectF


class SubwayGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("술취한 취객 OUT!")
        self.resize(800, 600)
        self.setFocusPolicy(Qt.StrongFocus)

        # 플레이어 설정
        self.player_x = 400
        self.player_y = 500
        self.player_radius = 20

        # 구조물 설정 (기둥, 벤치 등) ← 이걸 먼저 정의해야 함!
        self.obstacles = [
            QRectF(200, 200, 30, 100),  # 기둥
            QRectF(500, 400, 100, 20),  # 벤치
            QRectF(300, 100, 200, 20),  # 위쪽 선반
        ]

        # 취객 설정
        self.drunks = []
        self.spawn_drunks()  # ← 이건 obstacles가 정의된 다음에 와야 함

        # 상태 변수
        self.result_msg = ""
        self.game_active = True

        # 게임 루프
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(30)

        self.show()


    def spawn_drunks(self):
        self.drunks.clear()
        for _ in range(5):
            while True:
                x = random.randint(50, 750)
                y = random.randint(50, 500)
                new_rect = QRectF(x, y, 40, 40)
                # 구조물과 겹치지 않게 배치 (intersects로 수정)
                if not any(ob.intersects(new_rect) for ob in self.obstacles):
                    self.drunks.append(new_rect)
                    break


    def paintEvent(self, event):
        qp = QPainter(self)

        # 배경
        qp.fillRect(self.rect(), QColor(230, 230, 230))

        # 구조물 그리기
        qp.setBrush(QColor(180, 180, 180))
        for ob in self.obstacles:
            qp.drawRect(ob)

        # 플레이어 (직원)
        qp.setBrush(QColor(0, 100, 255))
        qp.drawEllipse(self.player_x - self.player_radius,
                       self.player_y - self.player_radius,
                       self.player_radius * 2, self.player_radius * 2)

        # 취객
        qp.setBrush(QColor(255, 50, 50))
        for drunk in self.drunks:
            qp.drawRect(drunk)

        # 메시지
        if self.result_msg:
            qp.setFont(QFont("Arial", 24))
            qp.setPen(QColor(0, 0, 0))
            qp.drawText(250, 100, self.result_msg)

    def keyPressEvent(self, event):
        if not self.game_active:
            if event.key() == Qt.Key_Space:
                self.restart_game()
            return

        speed = 20  # ← 이동 속도 조절 여기서!

        dx = 0
        dy = 0
        if event.key() == Qt.Key_Left:
            dx = -speed
        elif event.key() == Qt.Key_Right:
            dx = speed
        elif event.key() == Qt.Key_Up:
            dy = -speed
        elif event.key() == Qt.Key_Down:
            dy = speed

        new_x = self.player_x + dx
        new_y = self.player_y + dy
        player_rect = QRectF(new_x - self.player_radius, new_y - self.player_radius,
                            self.player_radius * 2, self.player_radius * 2)

        if not any(ob.intersects(player_rect) for ob in self.obstacles):
            self.player_x = new_x
            self.player_y = new_y

        self.player_x = max(self.player_radius, min(self.width() - self.player_radius, self.player_x))
        self.player_y = max(self.player_radius, min(self.height() - self.player_radius, self.player_y))


    def update_game(self):
        if not self.game_active:
            return

        player_rect = QRectF(
            self.player_x - self.player_radius,
            self.player_y - self.player_radius,
            self.player_radius * 2,
            self.player_radius * 2
        )

        new_drunks = []
        for drunk in self.drunks:
            if player_rect.intersects(drunk):
                continue
            new_drunks.append(drunk)
        self.drunks = new_drunks

        if not self.drunks:
            self.result_msg = "모든 취객 퇴치 성공! 🎉"
            self.game_active = False

        self.update()

    def restart_game(self):
        self.player_x = 400
        self.player_y = 500
        self.result_msg = ""
        self.game_active = True
        self.spawn_drunks()
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SubwayGame()
    sys.exit(app.exec_())
