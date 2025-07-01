import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QPoint


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mouse Follower Ball')
        self.setMouseTracking(True)  # 마우스 추적 활성화
        self.resize(1280, 720)
        self.ball_pos = QPoint(-100, -100)  # 처음에는 화면 밖에 숨김
        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setBrush(QColor(0, 0, 255))  # 파란색
        radius = 30
        qp.drawEllipse(self.ball_pos, radius, radius)

    def mouseMoveEvent(self, event):
        self.ball_pos = event.pos()
        self.update()  # 다시 그리기 요청

    def enterEvent(self, event):
        self.setMouseTracking(True)

    def leaveEvent(self, event):
        self.ball_pos = QPoint(-100, -100)  # 화면 밖으로 보냄
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
