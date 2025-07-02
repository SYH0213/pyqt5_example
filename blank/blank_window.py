## Ex 3-1. 창 띄우기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):

    def __init__(self):
        #super -> 부모 클래스
        super().__init__()
        self.initUI()

    def initUI(self):
        #창의 이름 설정
        self.setWindowTitle('WindowTitle')
        #창을 띄우는 위치
        self.move(0, 0)
        #창 크기 설정
        self.resize(1280, 720)
        #위의 설정대로 창을 생성
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())

