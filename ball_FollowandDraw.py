import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint, QTimer


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ball + Drawing')
        self.setMouseTracking(True)
        self.resize(1280, 720)

        self.ball_pos = QPoint(-100, -100)
        self.ball_color = QColor(0, 0, 255)
        self.follow_mouse = True

        self.gravity_enabled = False
        self.gravity = 1.0
        self.velocity = 0.0
        self.timer = QTimer()
        self.timer.timeout.connect(self.apply_gravity)

        # 선 그리기 관련
        self.drawing = False
        self.lines = []  # 선을 이루는 (시작점, 끝점) 리스트
        self.last_point = None

        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)

        # 공 그리기
        qp.setBrush(self.ball_color)
        qp.drawEllipse(self.ball_pos, 30, 30)

        # 선 그리기
        pen = QPen(Qt.black, 3)
        qp.setPen(pen)
        for start, end in self.lines:
            qp.drawLine(start, end)

    def mouseMoveEvent(self, event):
        if self.follow_mouse:
            self.ball_pos = event.pos()
            self.update()

        if self.drawing and self.last_point:
            current_point = event.pos()
            self.lines.append((self.last_point, current_point))
            self.last_point = current_point
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.follow_mouse:
                self.drawing = True
                self.last_point = event.pos()
            else:
                self.follow_mouse = False
                self.gravity_enabled = True
                self.ball_color = QColor(255, 0, 0)
                self.velocity = 0.0
                self.timer.start(16)

        elif event.button() == Qt.RightButton:
            self.follow_mouse = True
            self.gravity_enabled = False
            self.ball_color = QColor(0, 0, 255)
            self.timer.stop()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            self.last_point = None

    def apply_gravity(self):
        if self.gravity_enabled:
            self.velocity += self.gravity
            new_y = self.ball_pos.y() + self.velocity
            max_y = self.height() - 30
            if new_y > max_y:
                new_y = max_y
                self.velocity = 0
            self.ball_pos.setY(int(new_y))
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
