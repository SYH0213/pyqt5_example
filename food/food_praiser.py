import sys
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDialog,
    QFileDialog, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt

PRAISES = [
    "이 조합… 거의 한식계의 피카소입니다.",
    "탄단지 비율이 이토록 아름다울 수 있나요?",
    "색감 배치가 완벽합니다. 셰프세요?",
    "영양과 예술의 완벽한 조화… 감탄만 나옵니다.",
    "이건 그냥 식사가 아니라 작품입니다.",
    "미슐랭 셰프도 감동할 만찬이에요!"
]

class PraiseDialog(QDialog):
    def __init__(self, praise_text, gif_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎉 칭찬 팝업")
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #fff;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # 칭찬 문구
        self.label_text = QLabel(praise_text)
        self.label_text.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        self.label_text.setAlignment(Qt.AlignCenter)
        self.label_text.setWordWrap(True)

        # GIF
        self.label_gif = QLabel()
        self.label_gif.setFixedSize(200, 200)
        self.label_gif.setAlignment(Qt.AlignCenter)
        self.label_gif.setScaledContents(True)

        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(self.label_gif.size())
            self.label_gif.setMovie(self.movie)
            self.movie.start()
        else:
            self.label_gif.setText("❌ clap.gif 없음")

        layout.addWidget(self.label_gif)
        layout.addWidget(self.label_text)
        self.setLayout(layout)

class FoodPraiseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍚 밥 먹고 칭찬받기 앱")
        self.resize(500, 650)
        self.setStyleSheet("background-color: #f9f9f9;")

        self.current_image_path = None

        self.label_image = QLabel("음식 사진을 업로드해주세요.")
        self.label_image.setFixedSize(400, 250)
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setScaledContents(True)
        self.label_image.setStyleSheet("border: 2px dashed #aaa; color: #777;")

        self.btn_upload = QPushButton("📷 음식 사진 업로드")
        self.btn_upload.clicked.connect(self.upload_image)

        self.btn_praise = QPushButton("🤖 칭찬받기")
        self.btn_praise.clicked.connect(self.show_praise)
        self.btn_praise.setEnabled(False)

        button_style = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            font-size: 15px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:disabled {
            background-color: #ccc;
            color: #888;
        }
        """
        self.btn_upload.setStyleSheet(button_style)
        self.btn_praise.setStyleSheet(button_style)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(15)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.label_image)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.btn_praise)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *webp)"
        )
        if file_path:
            pixmap = QPixmap(file_path)
            self.label_image.setPixmap(pixmap)
            self.current_image_path = file_path
            self.btn_praise.setEnabled(True)

    def show_praise(self):
        if not self.current_image_path:
            QMessageBox.warning(self, "주의", "먼저 사진을 업로드해주세요!")
            return

        praise = random.choice(PRAISES)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(base_dir, "temp", "clap.gif")

        dialog = PraiseDialog(praise, gif_path, self)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FoodPraiseApp()
    win.show()
    sys.exit(app.exec_())
