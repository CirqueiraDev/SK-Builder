from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BuildLogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Building...")
        self.setFixedSize(450, 300)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #111;
                border: 1px solid #333;
            }
            QLabel {
                color: #ff4444;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #000;
                color: #0f0;
                border: 1px solid #222;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
            QPushButton {
                background-color: #222;
                border: 1px solid #444;
                padding: 6px;
                color: #ddd;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("Build Process")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Consolas", 12, QFont.Bold))

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setEnabled(False)

        layout.addWidget(title)
        layout.addWidget(self.log_box)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def add_log(self, text: str):
        self.log_box.append(text)
        self.log_box.verticalScrollBar().setValue(
            self.log_box.verticalScrollBar().maximum()
        )

    def finish(self):
        self.add_log("\nBuild finished!")
        self.close_btn.setEnabled(True)
