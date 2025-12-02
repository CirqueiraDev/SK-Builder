from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon
from src.styles import MAIN_STYLE, SIDEBAR_STYLE, TOPBAR_STYLE, close_btn_style, control_btn_style
from src.pages.options_page import OptionsPage
from src.pages.builder_page import BuilderPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("./logos/sk_logo.png"))
        self.setWindowTitle("SK Builder")
        self.setGeometry(100, 50, 1100, 620)
        self.setStyleSheet(MAIN_STYLE)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.dragging = False
        self.offset = QPoint()

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar = self.create_top_bar()
        
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        
        self.sidebar = self.create_sidebar()
        
        self.stack = QStackedWidget()
        self.options_page = OptionsPage()
        self.builder_page = BuilderPage(self.options_page)
        
        self.stack.addWidget(self.options_page)
        self.stack.addWidget(self.builder_page)
        
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.stack)

        main_layout.addWidget(top_bar)
        main_layout.addLayout(body_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)

        self.fade_anim = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(2000)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.setEasingCurve(QEasingCurve.InOutQuad)

    def create_top_bar(self):
        top_bar = QFrame()
        top_bar.setFixedHeight(35)
        top_bar.setStyleSheet(TOPBAR_STYLE)
        
        top_bar.mousePressEvent = self.topbar_mousePressEvent
        top_bar.mouseMoveEvent = self.topbar_mouseMoveEvent
        top_bar.mouseReleaseEvent = self.topbar_mouseReleaseEvent
        
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(15, 0, 10, 0)
        top_layout.setSpacing(10)
        
        icon_label = QLabel("😈")
        icon_label.setStyleSheet("color: #ff4444; font-size: 16px;")
        
        title = QLabel("SK Builder")
        title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title.setStyleSheet("color: #e0e0e0;")
        
        version = QLabel("v0.2.5")
        version.setStyleSheet("color: #666; font-size: 9px;")
        
        top_layout.addWidget(icon_label)
        top_layout.addWidget(title)
        top_layout.addWidget(version)
        top_layout.addStretch()

        btn_minimize = QPushButton("🟡")
        btn_close = QPushButton("🔴")
        
        btn_minimize.setStyleSheet(control_btn_style)
        btn_close.setStyleSheet(close_btn_style)
        
        btn_minimize.clicked.connect(self.showMinimized)
        btn_close.clicked.connect(self.close)
        
        top_layout.addWidget(btn_minimize)
        top_layout.addWidget(btn_close)
        
        top_bar.setLayout(top_layout)
        return top_bar
    
    def topbar_mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()
    
    def topbar_mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)
    
    def topbar_mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet(SIDEBAR_STYLE)
        
        side_layout = QVBoxLayout()
        side_layout.setContentsMargins(10, 20, 10, 20)
        side_layout.setSpacing(5)

        self.btn_options = QPushButton("Options")
        self.btn_builder = QPushButton("Builder")

        self.btn_options.setObjectName("active")

        self.btn_options.clicked.connect(lambda: self.switch_page(0, self.btn_options))
        self.btn_builder.clicked.connect(lambda: self.switch_page(1, self.btn_builder))
        
        side_layout.addWidget(self.btn_options)
        side_layout.addWidget(self.btn_builder)
        side_layout.addStretch()
        
        footer = QLabel("github.com/CirqueiraDev")
        footer.setStyleSheet("color: #ff4444; font-size: 10px;")
        footer.setAlignment(Qt.AlignCenter)
        side_layout.addWidget(footer)
        
        sidebar.setLayout(side_layout)
        return sidebar

    def switch_page(self, index, button):
        for btn in [self.btn_options, self.btn_builder]:
            btn.setObjectName("")
            btn.setStyleSheet("")
        
        button.setObjectName("active")
        button.setStyleSheet(MAIN_STYLE)
        
        self.stack.setCurrentIndex(index)

    def show_message(self, message):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Info", message)

    def showEvent(self, event):
        super().showEvent(event)
        self.fade_anim.start()