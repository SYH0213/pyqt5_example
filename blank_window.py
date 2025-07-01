## Ex 3-1. 창 띄우기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):

    def __init__(self):
        #super -> 부모 클래스
        super().__init__()
        self.initUI()

    def initUI(self):
        #창이름
        self.setWindowTitle('WindowTitle')
        #창위치
        self.move(0, 0)
        #창크기
        self.resize(1280, 720)
        #창띄우기
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())

