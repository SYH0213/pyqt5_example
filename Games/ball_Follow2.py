import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mouse Follower Ball with Gravity')
        self.setMouseTracking(True)
        self.resize(1280, 720)

        # 공 관련 변수
        self.ball_pos = QPoint(-100, -100)
        self.ball_color = QColor(0, 0, 255)  # 기본은 파란색
        self.follow_mouse = True  # 마우스를 따라다니는지 여부

        # 중력 관련 변수
        self.gravity_enabled = False
        self.gravity = 1.0
        self.velocity = 0.0

        # 중력 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.apply_gravity)

        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setBrush(self.ball_color)
        radius = 30
        qp.drawEllipse(self.ball_pos, radius, radius)

    def mouseMoveEvent(self, event):
        if self.follow_mouse:
            self.ball_pos = event.pos()
            self.update()

    def enterEvent(self, event):
        self.setMouseTracking(True)

    def leaveEvent(self, event):
        if self.follow_mouse:
            self.ball_pos = QPoint(-100, -100)
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 왼쪽 클릭: 중력 모드
            self.follow_mouse = False
            self.gravity_enabled = True
            self.ball_color = QColor(255, 0, 0)  # 빨간색
            self.velocity = 0.0
            self.timer.start(16)

        elif event.button() == Qt.RightButton:
            # 오른쪽 클릭: 다시 마우스를 따라다니게 설정
            self.follow_mouse = True
            self.gravity_enabled = False
            self.ball_color = QColor(0, 0, 255)  # 파란색
            self.timer.stop()
            self.update()


    def apply_gravity(self):
        if self.gravity_enabled:
            self.velocity += self.gravity
            new_y = self.ball_pos.y() + self.velocity
            max_y = self.height() - 30  # 바닥 범위 제한 (반지름 고려)

            if new_y > max_y:
                new_y = max_y
                self.velocity = 0  # 바닥 도착 시 정지

            self.ball_pos.setY(int(new_y))
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
