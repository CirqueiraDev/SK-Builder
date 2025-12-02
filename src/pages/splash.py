from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QGraphicsOpacityEffect
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from src.styles import MAIN_STYLE

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setGeometry(95, 50, 1100, 620)

        # Container
        layout = QVBoxLayout(self)

        # Fundo estiloso
        self.setStyleSheet(MAIN_STYLE)

        # Texto
        self.text = QLabel("SK Stealer by @CirqueiraDev")
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setFont(QFont("Segoe UI", 16, QFont.Bold))

        layout.addWidget(self.text)

        # Fade effect
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

        self.anim.finished.connect(self.fade_out)

    def start(self):
        self.show()
        self.anim.start()

    def fade_out(self):
        QTimer.singleShot(1200, self._start_fade_out)

    def _start_fade_out(self):
        self.anim2 = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim2.setDuration(1000)
        self.anim2.setStartValue(1)
        self.anim2.setEndValue(0)
        self.anim2.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim2.finished.connect(self.close)
        self.anim2.start()
