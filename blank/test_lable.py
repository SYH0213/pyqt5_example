## Ex 5-2. QLabel.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label1 = QLabel('First Label', self)
        label1.setAlignment(Qt.AlignCenter)

        label2 = QLabel('Second Label', self)
        label2.setAlignment(Qt.AlignVCenter)

        # 기본 폰트 설정을 가져와서
        font1 = label1.font()
        font1.setPointSize(20)
        
        # 기본 폰트 설정을 읽어와서
        font2 = label2.font()
        # 폰트를 'Times New Roman'으로 변경
        font2.setFamily('Times New Roman')
        # 굵은 폰트로 변경
        font2.setBold(True)

        # label1에 font1설정 적용
        label1.setFont(font1)
        # label2에 font2설정 적용
        label2.setFont(font2)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)

        self.setLayout(layout)

        self.setWindowTitle('QLabel')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
