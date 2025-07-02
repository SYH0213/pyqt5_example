import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QRadioButton, QButtonGroup, QPushButton, QMessageBox

class SurveyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("간단 설문 시스템")
        self.setGeometry(100, 100, 300, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # 질문 1
        self.q1_label = QLabel("1. 오늘 기분은 어떠신가요?")
        self.q1_group = QButtonGroup(self)
        self.q1_good = QRadioButton("좋음")
        self.q1_bad = QRadioButton("나쁨")
        self.q1_group.addButton(self.q1_good)
        self.q1_group.addButton(self.q1_bad)

        layout.addWidget(self.q1_label)
        layout.addWidget(self.q1_good)
        layout.addWidget(self.q1_bad)

        # 제출 버튼
        self.submit_btn = QPushButton("제출")
        self.submit_btn.clicked.connect(self.submit)

        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def submit(self):
        if self.q1_good.isChecked():
            answer = "좋음"
        elif self.q1_bad.isChecked():
            answer = "나쁨"
        else:
            QMessageBox.warning(self, "오류", "답을 선택해주세요.")
            return

        QMessageBox.information(self, "설문 완료", f"설문 감사합니다!\n응답: {answer}")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SurveyApp()
    window.show()
    sys.exit(app.exec_())
