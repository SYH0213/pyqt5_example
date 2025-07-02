import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtCore import QTimer
from pynput import keyboard
import threading

class KeyLogger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("전역 키 입력 추적기")
        self.resize(400, 300)

        self.key_counts = {}
        # 경로 설정 부분 시작
        self.log_folder = r"C:\Users\SBA\github\pyqt5_example\test\log"
        os.makedirs(self.log_folder, exist_ok=True)
        self.log_file = os.path.join(self.log_folder, "keylog.txt")
        # 경로 설정 부분 끝


        # UI
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.btn_show = QPushButton("입력 통계 보기", self)
        self.btn_reset = QPushButton("기록 초기화", self)

        self.btn_show.clicked.connect(self.show_counts)
        self.btn_reset.clicked.connect(self.reset_counts)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.btn_show)
        layout.addWidget(self.btn_reset)
        self.setLayout(layout)

        self.load_from_file()

        # UI 주기적 갱신용 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text_edit)
        self.timer.start(1000)

        # 백그라운드 키 리스너 시작
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener_thread = threading.Thread(target=self.listener.start)
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def on_key_press(self, key):
        try:
            key_str = key.char.upper()
        except AttributeError:
            key_str = str(key).replace("Key.", "").capitalize()

        # 항상 누적
        self.key_counts[key_str] = self.key_counts.get(key_str, 0) + 1
        self.save_to_file()

    def save_to_file(self):
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                for key, count in self.key_counts.items():
                    f.write(f"{key}:{count}\n")
        except Exception as e:
            print(f"파일 저장 오류: {e}")

    def load_from_file(self):
        if not os.path.exists(self.log_file):
            return
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if ':' in line:
                        key, count = line.strip().split(":")
                        self.key_counts[key] = int(count)
        except Exception as e:
            print(f"파일 읽기 오류: {e}")

    def update_text_edit(self):
        if not self.key_counts:
            self.text_edit.setPlainText("아직 입력된 키가 없습니다.")
        else:
            sorted_counts = sorted(self.key_counts.items(), key=lambda x: x[1], reverse=True)
            result = "\n".join(f"{k} : {v}회" for k, v in sorted_counts)
            self.text_edit.setPlainText(result)

    def show_counts(self):
        if not self.key_counts:
            QMessageBox.information(self, "입력 통계", "입력된 키가 없습니다.")
            return

        sorted_counts = sorted(self.key_counts.items(), key=lambda x: x[1], reverse=True)
        result = "\n".join(f"{key} : {count}회" for key, count in sorted_counts)
        QMessageBox.information(self, "입력 통계", result)

    def reset_counts(self):
        self.key_counts.clear()
        if os.path.exists(self.log_file):
            try:
                os.remove(self.log_file)
                QMessageBox.information(self, "초기화", "기록이 초기화되었습니다.")
            except Exception as e:
                QMessageBox.warning(self, "오류", f"파일 삭제 실패: {e}")
        self.update_text_edit()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = KeyLogger()
    win.show()
    sys.exit(app.exec_())
