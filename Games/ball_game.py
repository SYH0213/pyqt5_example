import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPoint, QTimer, QRect


class DropGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drop the Ball!")
        self.setMouseTracking(True)
        self.resize(800, 600)

        # 공
        self.ball_pos = QPoint(-100, -100)
        self.ball_radius = 30
        self.ball_color = QColor(0, 0, 255)
        self.follow_mouse = True

        # 중력
        self.gravity_enabled = False
        self.gravity = 1.0
        self.velocity = 0.0
        self.timer = QTimer()
        self.timer.timeout.connect(self.apply_gravity)

        # 바구니
        self.basket_rect = QRect(300, 550, 200, 30)

        # 결과 메시지
        self.result_msg = ""

        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)

        # 공 그리기
        qp.setBrush(self.ball_color)
        qp.drawEllipse(self.ball_pos, self.ball_radius, self.ball_radius)

        # 바구니 그리기
        qp.setBrush(QColor(100, 100, 100))
        qp.drawRect(self.basket_rect)

        # 메시지 출력
        if self.result_msg:
            qp.setPen(QColor(0, 0, 0))
            qp.setFont(QFont("Arial", 20))
            qp.drawText(300, 100, self.result_msg)

    def mouseMoveEvent(self, event):
        if self.follow_mouse:
            self.ball_pos = event.pos()
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.follow_mouse:
            # 낙하 시작
            self.follow_mouse = False
            self.gravity_enabled = True
            self.ball_color = QColor(255, 0, 0)
            self.velocity = 0.0
            self.result_msg = ""
            self.timer.start(16)

        elif event.button() == Qt.RightButton:
            # 리셋
            self.follow_mouse = True
            self.gravity_enabled = False
            self.ball_color = QColor(0, 0, 255)
            self.result_msg = ""
            self.timer.stop()
            self.update()

    def apply_gravity(self):
        if self.gravity_enabled:
            self.velocity += self.gravity
            new_y = self.ball_pos.y() + self.velocity
            if new_y > self.height() - self.ball_radius:
                new_y = self.height() - self.ball_radius
                self.gravity_enabled = False
                self.timer.stop()
                self.check_success()
            self.ball_pos.setY(int(new_y))
            self.update()

    def check_success(self):
        # 공 중심 좌표가 바구니 안에 들어가 있는지 확인
        center_x = self.ball_pos.x()
        center_y = self.ball_pos.y()
        if self.basket_rect.contains(center_x, center_y):
            self.result_msg = "성공! 🎉"
        else:
            self.result_msg = "실패 😢"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = DropGame()
    sys.exit(app.exec_())
