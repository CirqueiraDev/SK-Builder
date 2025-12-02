from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QIcon
from src.styles import MAIN_STYLE, TOPBAR_STYLE, close_btn_style


class CustomMessageBox(QMainWindow):
    def __init__(self, icon: str, title: str, message: str):
        super().__init__()
        self.setWindowIcon(QIcon("./logos/sk_logo.png"))
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(500, 250, 300, 150)
        self.setStyleSheet(MAIN_STYLE)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.dragging = False
        self.offset = QPoint()

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar = self.create_top_bar(icon, title)

        body = QFrame()
        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(20, 20, 20, 20)

        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignCenter)
        msg_label.setStyleSheet("color: #eee; font-size: 13px;")

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border-radius: 6px;
                padding: 6px 14px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        ok_button.clicked.connect(self.close)

        body_layout.addWidget(msg_label)
        body_layout.addWidget(ok_button, alignment=Qt.AlignCenter)
        body.setLayout(body_layout)

        main_layout.addWidget(top_bar)
        main_layout.addWidget(body)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_top_bar(self, icon: str, title: str):
        top_bar = QFrame()
        top_bar.setFixedHeight(35)
        top_bar.setStyleSheet(TOPBAR_STYLE)

        top_bar.mousePressEvent = self.mousePressEvent
        top_bar.mouseMoveEvent = self.mouseMoveEvent
        top_bar.mouseReleaseEvent = self.mouseReleaseEvent

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(15, 0, 10, 0)
        top_layout.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("color: #ff4444; font-size: 16px;")

        title = QLabel(title)
        title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title.setStyleSheet("color: #e0e0e0;")

        top_layout.addWidget(icon_label)
        top_layout.addWidget(title)
        top_layout.addStretch()

        btn_close = QPushButton("🔴")
        btn_close.setStyleSheet(close_btn_style)
        btn_close.clicked.connect(self.close)

        top_layout.addWidget(btn_close)
        top_bar.setLayout(top_layout)
        return top_bar


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False
